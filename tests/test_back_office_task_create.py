from datetime import datetime
from unittest.mock import MagicMock

from gradient_labs import (
    Client,
    BackOfficeTask,
    BackOfficeTaskStatus,
    BackOfficeTaskCreateParams,
    BackOfficeTaskCreateAttachment,
)

AGENT_ID = "agent_01ham6bzcdeja9xzqhjf6daq30"
PROCEDURE_ID = "proc_01ham6bzcdeja9xzqhjf6daq30"


def _client_returning(response: dict):
    client = Client(api_key="test-key")
    post = MagicMock(return_value=response)
    client.http_client.post = post
    return client, post


def _pending_response() -> dict:
    return {
        "id": "task-123",
        "agent_id": AGENT_ID,
        "status": "pending",
        "input": {"order_id": "order-456"},
        "created": "2024-01-15T10:30:00",
    }


def test_create_back_office_task():
    client, post = _client_returning(_pending_response())

    task = client.create_back_office_task(
        params=BackOfficeTaskCreateParams(
            id="task-123",
            agent_id=AGENT_ID,
            procedure_id=PROCEDURE_ID,
            input={"order_id": "order-456"},
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert kwargs["path"] == "back-office-tasks"
    assert body["agent_id"] == AGENT_ID
    assert body["procedure_id"] == PROCEDURE_ID
    assert body["input"] == {"order_id": "order-456"}

    assert isinstance(task, BackOfficeTask)
    assert task.agent_id == AGENT_ID
    assert task.status == BackOfficeTaskStatus.PENDING


def test_create_back_office_task_includes_optional_fields():
    client, post = _client_returning(_pending_response())

    client.create_back_office_task(
        params=BackOfficeTaskCreateParams(
            id="task-123",
            agent_id=AGENT_ID,
            procedure_id=PROCEDURE_ID,
            input={"order_id": "order-456"},
            created=datetime(2024, 1, 15, 10, 30, 0),
            metadata={"team": "billing"},
            attachments=[
                BackOfficeTaskCreateAttachment(
                    file_name="document.pdf",
                    url="https://example.com/document.pdf",
                )
            ],
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert body["procedure_id"] == PROCEDURE_ID
    assert body["metadata"] == {"team": "billing"}
    assert body["created"] == "2024-01-15T10:30:00.000000Z"
    assert body["attachments"][0]["file_name"] == "document.pdf"
    assert body["attachments"][0]["url"] == "https://example.com/document.pdf"
