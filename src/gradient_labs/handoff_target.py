from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class HandOffTarget:
    # ID is your identifier of choice for this hand-off target. Can be anything consisting
    # of letters, numbers, or any of the following characters: `_` `-` `+` `=`.
    id: str

    # name is the hand-off target’s name.
    name: str

    # ref is a short reference for this target that never changes. It is stored in
    # lowercase and is unique within your company.
    ref: Optional[str] = None
