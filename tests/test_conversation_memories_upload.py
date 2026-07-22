from unittest.mock import MagicMock

from gradient_labs import Client, BulkUploadMemoriesParams

CONVERSATION_ID = "conv_01ham6bzcdeja9xzqhjf6daq30"


def _client(response):
    client = Client(api_key="test-key")
    post = MagicMock(return_value=response)
    client.http_client.post = post
    return client, post


def test_bulk_upload_conversation_memories():
    client, post = _client(
        {"upload_id": "upl_123", "memories_inserted": 2},
    )

    rsp = client.bulk_upload_conversation_memories(
        conversation_id=CONVERSATION_ID,
        params=BulkUploadMemoriesParams(
            idempotency_key="key-1",
            memories=[{"note": "prefers email"}, {"tier": "premium"}],
        ),
    )

    _, kwargs = post.call_args
    assert kwargs["path"] == f"conversations/{CONVERSATION_ID}/memories"
    body = kwargs["body"]
    assert body["idempotency_key"] == "key-1"
    assert body["memories"] == [{"note": "prefers email"}, {"tier": "premium"}]
    assert "created_at_keys" not in body

    assert rsp.upload_id == "upl_123"
    assert rsp.memories_inserted == 2


def test_bulk_upload_conversation_memories_includes_created_at_keys():
    client, post = _client(
        {"upload_id": "upl_456", "memories_inserted": 1},
    )

    client.bulk_upload_conversation_memories(
        conversation_id=CONVERSATION_ID,
        params=BulkUploadMemoriesParams(
            idempotency_key="key-2",
            memories=[{"event": "signup"}],
            created_at_keys=["occurred_at", "created_at"],
        ),
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert body["created_at_keys"] == ["occurred_at", "created_at"]
