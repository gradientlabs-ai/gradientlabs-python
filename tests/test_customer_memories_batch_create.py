from datetime import datetime
from unittest.mock import MagicMock

from gradient_labs import Client, CustomerMemory

CUSTOMER_ID = "cust_01ham6bzcdeja9xzqhjf6daq30"


def _client(response=None):
    client = Client(api_key="test-key")
    post = MagicMock(return_value=response)
    client.http_client.post = post
    return client, post


def test_batch_create_customer_memories():
    client, post = _client()

    rsp = client.batch_create_customer_memories(
        customer_id=CUSTOMER_ID,
        memories=[
            CustomerMemory(
                external_id="order_123",
                custom_type="order",
                created_at=datetime(2026, 7, 1, 10, 0, 0),
                data={"total": 42.0},
            ),
            CustomerMemory(
                external_id="pref_1",
                created_at=datetime(2026, 7, 2, 11, 30, 0),
                data={"channel": "email"},
            ),
        ],
    )

    assert rsp is None

    _, kwargs = post.call_args
    assert kwargs["path"] == f"customers/{CUSTOMER_ID}/memories"
    memories = kwargs["body"]["memories"]
    assert len(memories) == 2

    assert memories[0]["external_id"] == "order_123"
    assert memories[0]["custom_type"] == "order"
    assert memories[0]["created_at"] == "2026-07-01T10:00:00.000000Z"
    assert memories[0]["data"] == {"total": 42.0}


def test_batch_create_customer_memories_omits_optional_custom_type():
    client, post = _client()

    client.batch_create_customer_memories(
        customer_id=CUSTOMER_ID,
        memories=[
            CustomerMemory(
                external_id="pref_1",
                created_at=datetime(2026, 7, 2, 11, 30, 0),
                data={"channel": "email"},
            ),
        ],
    )

    _, kwargs = post.call_args
    memory = kwargs["body"]["memories"][0]
    assert memory["external_id"] == "pref_1"
    assert memory["created_at"] == "2026-07-02T11:30:00.000000Z"
    assert memory["data"] == {"channel": "email"}
    assert "custom_type" not in memory
