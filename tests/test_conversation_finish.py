from unittest.mock import MagicMock

from gradient_labs import Client, FinishParams

CONVERSATION_ID = "conv_01ham6bzcdeja9xzqhjf6daq30"


def _client():
    client = Client(api_key="test-key")
    put = MagicMock(return_value=None)
    client.http_client.put = put
    return client, put


def test_finish_conversation():
    client, put = _client()

    client.finish_conversation(
        conversation_id=CONVERSATION_ID,
        params=FinishParams(),
    )

    args, kwargs = put.call_args
    assert args[0] == f"conversations/{CONVERSATION_ID}/finish"
    assert kwargs["body"] == {}


def test_finish_conversation_includes_reason_code():
    client, put = _client()

    client.finish_conversation(
        conversation_id=CONVERSATION_ID,
        params=FinishParams(
            reason="Customer stopped replying",
            reason_code="customer-unresponsive",
        ),
    )

    _, kwargs = put.call_args
    body = kwargs["body"]
    assert body["reason"] == "Customer stopped replying"
    assert body["reason_code"] == "customer-unresponsive"


def test_finish_conversation_omits_reason_code_when_unset():
    client, put = _client()

    client.finish_conversation(
        conversation_id=CONVERSATION_ID,
        params=FinishParams(reason="Resolved"),
    )

    _, kwargs = put.call_args
    body = kwargs["body"]
    assert body["reason"] == "Resolved"
    assert "reason_code" not in body
