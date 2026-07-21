from typing import Optional
from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class FinishParams:
    # timestamp optionally defines the time when the conversation ended.
    # If not given, this will default to the current time.
    timestamp: Optional[datetime] = None

    # reason optionally allows you to describe why this conversation is finishing.
    reason: Optional[str] = None

    # reason_code optionally categorises why this conversation is finishing.
    # Valid values are "customer-ended-chat" and "customer-unresponsive".
    reason_code: Optional[str] = None


def finish_conversation(
    *, client: HttpClient, conversation_id: str, params: FinishParams
) -> None:
    body = {}
    if params.timestamp:
        body["timestamp"] = client.localize(params.timestamp)
    if params.reason:
        body["reason"] = params.reason
    if params.reason_code:
        body["reason_code"] = params.reason_code

    _ = client.put(
        f"conversations/{conversation_id}/finish",
        body=body,
    )
