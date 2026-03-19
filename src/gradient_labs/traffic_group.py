from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class TrafficGroupTarget:
    # target_type is the type of target (possible values: "procedure").
    target_type: str

    # target_id is the unique identifier of the target.
    target_id: str


@dataclass_json
@dataclass(frozen=True)
class TrafficGroup:
    # id is the unique identifier of the traffic group.
    id: str

    # name is the display name for the traffic group.
    name: str

    # targets is the list of targets assigned to the traffic group.
    targets: List[TrafficGroupTarget]
