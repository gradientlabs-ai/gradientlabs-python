import pytest
from datetime import datetime

from gradient_labs.types import Conversation


@pytest.fixture
def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def test_conversation(now_iso):
    body = {
        "id": "id-1234",
        "customer_id": "cust-456",
        "created": now_iso,
        "updated": now_iso,
        "metadata": {},
        "status": "open",
    }
    got = Conversation.from_dict(body)
