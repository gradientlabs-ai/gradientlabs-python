from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class UpsertHandOffTargetParams:
    # id is your identifier of choice for this hand-off target. Can be anything consisting
    # of letters, numbers, or any of the following characters: `_` `-` `+` `=`.
    id: str

    # name is the hand-off target’s name. This cannot be nil.
    name: str

    # ref is an optional short reference for this target that never changes, made of
    # letters, digits, `_` and `-`. It starts with a letter or digit, is at most 100
    # characters and is stored in lowercase. Leave it out to have one made from name.
    ref: Optional[str] = None


def upsert_hand_off_target(
    *, client: HttpClient, params: UpsertHandOffTargetParams
) -> None:
    _ = client.post(
        path="hand-off-targets",
        body={k: v for k, v in params.to_dict().items() if v is not None},
    )
