from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .traffic_group import TrafficGroup


@dataclass_json
@dataclass(frozen=True)
class TrafficGroupsList:
    traffic_groups: List[TrafficGroup]


def list_traffic_groups(*, client: HttpClient) -> TrafficGroupsList:
    """list_traffic_groups retrieves all traffic groups."""
    rsp = client.get(path="traffic-groups", body={})
    return TrafficGroupsList.from_dict(rsp)
