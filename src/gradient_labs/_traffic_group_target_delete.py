from ._http_client import HttpClient


def delete_traffic_group_target(
    *, client: HttpClient, traffic_group_id: str, target_id: str
) -> None:
    """delete_traffic_group_target removes a target from a traffic group."""
    _ = client.delete(
        path=f"traffic-groups/{traffic_group_id}/targets/{target_id}", body={}
    )
