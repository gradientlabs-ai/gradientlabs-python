from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .back_office_task import BackOfficeTask


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskCreateAttachment:
    file_name: str
    # Provide either url (remote file) or base64_contents (inline upload), not both.
    url: Optional[str] = None
    base64_contents: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskCreateParams:
    id: str
    agent_id: str
    input: Dict[str, Any]
    created: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None
    attachments: Optional[List[BackOfficeTaskCreateAttachment]] = None


def create_back_office_task(
    *, client: HttpClient, params: BackOfficeTaskCreateParams
) -> BackOfficeTask:
    body: Dict[str, Any] = {
        "id": params.id,
        "agent_id": params.agent_id,
        "input": params.input,
    }
    if params.created is not None:
        body["created"] = HttpClient.localize(params.created)
    if params.metadata is not None:
        body["metadata"] = params.metadata
    if params.attachments is not None:
        body["attachments"] = [a.to_dict() for a in params.attachments]
    rsp = client.post(path="back-office-tasks", body=body)
    return BackOfficeTask.from_dict(rsp)
