from ._http_client import HttpClient


def delete_back_office_task(*, client: HttpClient, task_id: str) -> None:
    _ = client.delete(
        path=f"back-office-tasks/{task_id}",
        body=None,
    )
