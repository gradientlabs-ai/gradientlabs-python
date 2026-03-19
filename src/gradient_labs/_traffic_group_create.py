from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .traffic_group import TrafficGroup


@dataclass_json
@dataclass(frozen=True)
class CreateTrafficGroupParams:
    # name is the display name for the traffic group.
    name: str


def create_traffic_group(
    *, client: HttpClient, params: CreateTrafficGroupParams
) -> TrafficGroup:
    """create_traffic_group creates a new traffic group."""
    body = {
        "name": params.name,
    }

    rsp = client.post(path="traffic-groups", body=body)
    return TrafficGroup.from_dict(rsp)
