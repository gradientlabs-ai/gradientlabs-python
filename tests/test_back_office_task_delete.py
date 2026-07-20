from unittest.mock import MagicMock

from gradient_labs import Client

TASK_ID = "task-123"


def _client():
    client = Client(api_key="test-key")
    delete = MagicMock(return_value=None)
    client.http_client.delete = delete
    return client, delete


def test_delete_back_office_task():
    client, delete = _client()

    result = client.delete_back_office_task(task_id=TASK_ID)

    _, kwargs = delete.call_args
    assert kwargs["path"] == f"back-office-tasks/{TASK_ID}"
    assert kwargs["body"] is None
    assert result is None
