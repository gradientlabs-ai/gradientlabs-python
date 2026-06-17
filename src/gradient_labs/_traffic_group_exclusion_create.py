from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .traffic_group import TrafficGroupTarget


@dataclass_json
@dataclass(frozen=True)
class TrafficGroupExclusionCreateParams:
    target_type: str
    target_id: str


def create_traffic_group_exclusion(
    *,
    client: HttpClient,
    group_id: str,
    params: TrafficGroupExclusionCreateParams,
) -> TrafficGroupTarget:
    body = {
        "target_type": params.target_type,
        "target_id": params.target_id,
    }
    rsp = client.post(path=f"traffic-groups/{group_id}/exclusions", body=body)
    return TrafficGroupTarget.from_dict(rsp)
