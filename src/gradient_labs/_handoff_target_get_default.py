from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .conversation import ConversationChannel


@dataclass_json
@dataclass(frozen=True)
class GetDefaultHandOffTargetParams:
    # channel is the conversation channel for which to get the default hand-off target.
    channel: ConversationChannel


@dataclass_json
@dataclass(frozen=True)
class GetDefaultHandOffTargetResponse:
    # id is the unique identifier for the default hand-off target.
    # Empty string if no default is set.
    id: str


def get_default_hand_off_target(
    *, client: HttpClient, params: GetDefaultHandOffTargetParams
) -> GetDefaultHandOffTargetResponse:
    rsp = client.get(
        path="hand-off-targets/default",
        query_params={"channel": params.channel.value},
    )
    return GetDefaultHandOffTargetResponse.from_dict(rsp)
