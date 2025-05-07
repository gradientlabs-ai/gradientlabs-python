from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .conversation import Conversation


@dataclass_json
@dataclass(frozen=True)
class ReadParams:
    # SupportPlatform is the name of the support platform where the
    # conversation was started (e.g. Intercom).
    #
    # Leave empty if the conversation was started via the Gradient
    # Labs API.
    support_platform: Optional[str] = None


def read_conversation(
    *, client: HttpClient, conversation_id: str, params: ReadParams
) -> None:
    body = {}
    if params.support_platform:
        body["support_platform"] = params.reason

    body = client.get(
        path=f"conversations/{conversation_id}/read",
        body={},
    )
    return Conversation.from_dict(body)
