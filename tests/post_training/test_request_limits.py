"""Training data size limits: per request and in flight, as on Tinker."""

import threading
import time

import pytest

from macrocosmos import post_training

from .fake_gateway import FakeGateway
from .test_post_training_client import MODEL, datum

REQUEST_ENV = "MACROCOSMOS_POST_TRAINING_MAX_REQUEST_BYTES"
INFLIGHT_ENV = "MACROCOSMOS_POST_TRAINING_MAX_INFLIGHT_BYTES"


def client(gw, **limits):
    return post_training.PostTrainingClient(
        api_key="test-key", base_url="http://gw.test", transport=gw.transport, **limits
    )


@pytest.fixture(autouse=True)
def no_limit_env(monkeypatch):
    monkeypatch.delenv(REQUEST_ENV, raising=False)
    monkeypatch.delenv(INFLIGHT_ENV, raising=False)


def test_limits_come_from_the_gateway_read_once():
    gw = FakeGateway()
    gw.client_config = {"max_request_bytes": 1_000_000, "max_inflight_bytes": 7_000_000}
    with client(gw) as c:
        assert c._gw.max_request_bytes == 1_000_000
        assert c._gw.max_inflight_bytes == 7_000_000
        assert c._gw.max_request_bytes == 1_000_000
    assert len(gw.calls("GET", r"/v1/client/config")) == 1


def test_the_gateway_is_asked_only_when_a_limit_is_needed():
    gw = FakeGateway()
    with client(gw) as c:
        c.create_lora_training_client(base_model=MODEL).result()
    assert gw.calls("GET", r"/v1/client/config") == []


def test_options_and_the_environment_override_the_gateway(monkeypatch):
    monkeypatch.setenv(REQUEST_ENV, "50_000_000")
    monkeypatch.setenv(INFLIGHT_ENV, "0")
    gw = FakeGateway()
    with client(gw) as c:
        assert c._gw.max_request_bytes == 50_000_000
        assert c._gw.max_inflight_bytes == 0
    with client(gw, max_request_bytes=45_000) as c:
        assert c._gw.max_request_bytes == 45_000
    assert gw.calls("GET", r"/v1/client/config") == []  # every limit was set


def test_a_gateway_without_the_limits_is_an_error():
    gw = FakeGateway()
    gw.client_config = {"max_request_bytes": 5 << 20}
    with client(gw) as c:
        with pytest.raises(post_training.PostTrainingError, match="max_inflight_bytes"):
            c._gw.max_inflight_bytes  # noqa: B018
    gw.client_config = {"max_request_bytes": "5MB", "max_inflight_bytes": 0}
    with client(gw) as c:
        with pytest.raises(ValueError, match="gateway's max_request_bytes"):
            c._gw.max_request_bytes  # noqa: B018


def test_bad_limits_fail_early(monkeypatch):
    with pytest.raises(ValueError, match="over 512 bytes"):
        client(FakeGateway(), max_request_bytes=100)
    with pytest.raises(ValueError, match=">= 0"):
        client(FakeGateway(), max_inflight_bytes=-1)
    monkeypatch.setenv(REQUEST_ENV, "5MB")
    with pytest.raises(ValueError, match="whole number of bytes"):
        client(FakeGateway())


def test_a_big_batch_fits_one_request_under_the_gateways_limit():
    gw = FakeGateway(max_body=5 << 20)
    with client(gw) as c:
        trainer = c.create_lora_training_client(base_model=MODEL).result()
        out = trainer.forward_backward(
            [datum(300) for _ in range(64)], loss_fn="importance_sampling"
        ).result()
    assert len(gw.calls("POST", r".+/forward_backward")) == 1
    assert len(out.loss_fn_outputs) == 64


def test_a_gateway_that_takes_less_says_how_to_lower_the_limit():
    gw = FakeGateway()  # 16 KB, like the old ingress
    with client(gw) as c:
        trainer = c.create_lora_training_client(base_model=MODEL).result()
        with pytest.raises(post_training.PayloadTooLargeError, match=REQUEST_ENV):
            trainer.forward_backward([datum(2000)], loss_fn="importance_sampling")


def test_sending_waits_while_the_in_flight_limit_is_full():
    gw = FakeGateway(max_body=20_000)
    gw.hold.add("forward_backward")
    # Each request carries one ~11 KB datum; three fit under the in-flight limit.
    with client(gw, max_request_bytes=20_000, max_inflight_bytes=35_000) as c:
        trainer = c.create_lora_training_client(base_model=MODEL).result()
        outcome = {}

        def train():
            future = trainer.forward_backward(
                [datum(600) for _ in range(6)], loss_fn="importance_sampling"
            )
            outcome["out"] = future.result()

        worker = threading.Thread(target=train)
        worker.start()
        time.sleep(1.0)
        assert len(gw.calls("POST", r".+/forward_backward")) == 3  # the rest wait

        gw.release()
        worker.join(timeout=30)
        assert not worker.is_alive()
        assert len(gw.calls("POST", r".+/forward_backward")) == 6
        assert len(outcome["out"].loss_fn_outputs) == 6
        assert trainer._inflight == {} and trainer._finished == {}


def test_no_in_flight_limit_sends_everything_at_once():
    gw = FakeGateway(max_body=20_000)
    gw.hold.add("forward_backward")
    with client(gw, max_request_bytes=20_000, max_inflight_bytes=0) as c:
        trainer = c.create_lora_training_client(base_model=MODEL).result()
        future = trainer.forward_backward(
            [datum(600) for _ in range(6)], loss_fn="importance_sampling"
        )
        assert len(gw.calls("POST", r".+/forward_backward")) == 6
        gw.release()
        assert len(future.result().loss_fn_outputs) == 6


def test_big_log_probs_are_fetched_from_their_signed_url():
    gw = FakeGateway(max_body=5_000_000, inline_logprobs_bytes=1_000)
    with client(gw) as c:
        trainer = c.create_lora_training_client(base_model=MODEL).result()
        out = trainer.forward_backward(
            [datum(300) for _ in range(4)], loss_fn="importance_sampling"
        ).result()
    assert [len(o["logprobs"].tolist()) for o in out.loss_fn_outputs] == [300] * 4
    [fetched] = gw.storage_requests
    assert "x-api-key" not in fetched.headers  # signed links never get the API key
