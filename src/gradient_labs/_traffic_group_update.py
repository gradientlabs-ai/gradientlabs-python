from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .traffic_group import TrafficGroup


@dataclass_json
@dataclass(frozen=True)
class UpdateTrafficGroupParams:
    # name is the new display name for the traffic group.
    name: str


def update_traffic_group(
    *, client: HttpClient, traffic_group_id: str, params: UpdateTrafficGroupParams
) -> TrafficGroup:
    """update_traffic_group updates an existing traffic group."""
    body = {
        "name": params.name,
    }

    rsp = client.put(path=f"traffic-groups/{traffic_group_id}", body=body)
    return TrafficGroup.from_dict(rsp)
