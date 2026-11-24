"""Getting saved adapters out, as on Tinker: save_weights_external, list_checkpoints,
signed URLs, and download."""

import json

import pytest

from macrocosmos import post_training
from macrocosmos.post_training import types

from .fake_gateway import FakeGateway

MODEL = "Qwen/Qwen3-4B"


@pytest.fixture
def gw():
    return FakeGateway()


@pytest.fixture
def trainer(gw):
    with post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport
    ) as client:
        yield client, client.create_lora_training_client(base_model=MODEL).result()


def test_tinkers_calls_give_signed_urls_for_a_saved_adapter(trainer):
    client, training_client = trainer
    saved = training_client.save_weights_external("final").result()
    assert isinstance(saved, types.SaveWeightsExternalResponse)
    response = (
        client.create_rest_client().get_external_weights_urls(saved.path).result()
    )
    assert set(response.urls) == {"adapter_config.json", "adapter_model.safetensors"}
    assert set(response.sha256) == set(response.urls)
    assert response.expires is not None


def test_list_checkpoints_shows_every_save_in_tinkers_shape(trainer):
    client, training_client = trainer
    training_client.save_weights_for_sampler("a").result()
    training_client.save_weights_for_sampler().result()  # a per-step rollout adapter
    listing = (
        client.create_rest_client().list_checkpoints(training_client.model_id).result()
    )
    ids = [c.checkpoint_id for c in listing.checkpoints]
    assert "adapters/named/a" in ids
    assert any(i.startswith("adapters/rollout-") for i in ids)
    assert all(
        c.tinker_path.startswith("mc://") and c.time is not None
        for c in listing.checkpoints
    )


def test_download_writes_the_peft_files(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    out = post_training.download(path, str(tmp_path / "adapter"), client=client)
    for name, data in gw.adapters[path].items():
        assert (tmp_path / "adapter" / name).read_bytes() == data
    config = json.loads((tmp_path / "adapter" / "adapter_config.json").read_text())
    assert config["peft_type"] == "LORA"
    assert out == str(tmp_path / "adapter")


def test_storage_never_receives_the_api_key(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    post_training.download(path, str(tmp_path), client=client)
    assert gw.storage_requests
    assert all("x-api-key" not in r.headers for r in gw.storage_requests)


def test_a_corrupted_file_is_refused_and_nothing_is_written(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    gw.adapters[path]["adapter_model.safetensors"] = b"tampered"  # after the save
    with pytest.raises(post_training.PostTrainingError, match="sha256"):
        post_training.download(path, str(tmp_path / "x"), client=client)
    assert not (tmp_path / "x").exists()


def test_an_unknown_checkpoint_is_not_found(trainer):
    client, training_client = trainer
    with pytest.raises(post_training.NotFoundError, match="checkpoint not found"):
        client.create_rest_client().get_external_weights_urls(
            f"mc://{training_client.model_id}/adapters/named/nope"
        )


def test_a_path_that_isnt_an_adapter_is_refused(trainer):
    client, _ = trainer
    with pytest.raises(ValueError, match="mc://"):
        client.create_rest_client().get_external_weights_urls("s3://bucket/key")


def test_the_rest_of_tinkers_rest_client_says_not_supported(trainer):
    client, _ = trainer
    rest = client.create_rest_client()
    with pytest.raises(post_training.NotSupportedError):
        rest.list_user_checkpoints()
    assert not hasattr(rest, "made_up_method")
