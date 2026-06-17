from ._http_client import HttpClient


def delete_traffic_group_exclusion(
    *, client: HttpClient, group_id: str, target_id: str
) -> None:
    client.delete(path=f"traffic-groups/{group_id}/exclusions/{target_id}", body={})
