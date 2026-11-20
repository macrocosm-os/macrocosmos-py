"""Getting saved adapters out, as on Tinker: save_weights_external, signed URLs, download."""

import hashlib
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
    urls = (
        client.create_rest_client().get_external_weights_urls(saved.path).result().urls
    )
    assert set(urls) == {
        "adapter_config.json",
        "adapter_model.safetensors",
        "manifest.json",
    }


def test_download_writes_the_peft_files_and_checks_them(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    out = post_training.download(path, str(tmp_path / "adapter"), client=client)
    manifest = json.loads((tmp_path / "adapter" / "manifest.json").read_text())
    for name, digest in manifest["sha256"].items():
        assert (
            hashlib.sha256((tmp_path / "adapter" / name).read_bytes()).hexdigest()
            == digest
        )
    assert out == str(tmp_path / "adapter")


def test_storage_never_receives_the_api_key(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    post_training.download(path, str(tmp_path), client=client)
    assert gw.storage_requests and all(
        "x-api-key" not in r.headers for r in gw.storage_requests
    )


def test_a_corrupted_file_is_refused(gw, trainer, tmp_path):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    gw.adapters[path]["adapter_model.safetensors"] = b"tampered"
    with pytest.raises(post_training.PostTrainingError, match="sha256"):
        post_training.download(path, str(tmp_path / "x"), client=client)
    assert not (tmp_path / "x").exists()  # nothing written


def test_an_unknown_adapter_is_not_found(trainer):
    client, _ = trainer
    with pytest.raises(post_training.NotFoundError):
        client.create_rest_client().get_external_weights_urls(
            "mc://nope-m0/adapters/named/x"
        )


def test_a_gateway_without_the_route_says_downloads_are_not_available(gw, trainer):
    client, training_client = trainer
    path = training_client.save_weights_for_sampler("final").result().path
    gw.downloads = False
    with pytest.raises(post_training.NotSupportedError, match="downloads"):
        client.create_rest_client().get_external_weights_urls(path)


def test_the_rest_of_tinkers_rest_client_says_not_supported(trainer):
    client, _ = trainer
    rest = client.create_rest_client()
    with pytest.raises(post_training.NotSupportedError):
        rest.list_checkpoints("run")
    assert not hasattr(rest, "made_up_method")
