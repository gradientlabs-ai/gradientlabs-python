from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .traffic_group import TrafficGroupTarget


@dataclass_json
@dataclass(frozen=True)
class CreateTrafficGroupTargetParams:
    # target_type is the type of target to add (possible values: "procedure").
    target_type: str

    # target_id is the unique identifier of the target to add to the group.
    target_id: str


def create_traffic_group_target(
    *,
    client: HttpClient,
    traffic_group_id: str,
    params: CreateTrafficGroupTargetParams,
) -> TrafficGroupTarget:
    """create_traffic_group_target adds a target to a traffic group."""
    body = {
        "target_type": params.target_type,
        "target_id": params.target_id,
    }

    rsp = client.post(path=f"traffic-groups/{traffic_group_id}/targets", body=body)
    return TrafficGroupTarget.from_dict(rsp)
