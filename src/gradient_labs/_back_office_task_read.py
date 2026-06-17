from ._http_client import HttpClient
from .back_office_task import BackOfficeTask


def read_back_office_task(*, client: HttpClient, task_id: str) -> BackOfficeTask:
    rsp = client.get(path=f"back-office-tasks/{task_id}/read", body={})
    return BackOfficeTask.from_dict(rsp)
