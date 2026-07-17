from unittest.mock import MagicMock

from gradient_labs import Client

CONVERSATION_ID = "conv_01ham6bzcdeja9xzqhjf6daq30"


def _client():
    client = Client(api_key="test-key")
    delete = MagicMock(return_value=None)
    client.http_client.delete = delete
    return client, delete


def test_delete_conversation():
    client, delete = _client()

    result = client.delete_conversation(conversation_id=CONVERSATION_ID)

    _, kwargs = delete.call_args
    assert kwargs["path"] == f"conversations/{CONVERSATION_ID}"
    assert kwargs["body"] is None
    assert result is None
