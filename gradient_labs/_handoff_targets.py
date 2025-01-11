from typing import List
from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class HandOffTarget:
    # ID is your identifier of choice for this hand-off target. Can be anything consisting
    # of letters, numbers, or any of the following characters: `_` `-` `+` `=`.
    id: str

    # name is the hand-off target’s name.
    name: str


@dataclass_json
@dataclass(frozen=True)
class HandOffTargets:
    targets: List[HandOffTarget]


def list_handoff_targets(*, client: HttpClient) -> HandOffTargets:
    rsp = client.get(
        path="hand-off-targets",
        body={},
    )
    return HandOffTargets.from_dict(rsp)
