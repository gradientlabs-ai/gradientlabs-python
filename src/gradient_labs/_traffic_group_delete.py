from ._http_client import HttpClient


def delete_traffic_group(*, client: HttpClient, traffic_group_id: str) -> None:
    """delete_traffic_group deletes a traffic group and all associated targets."""
    _ = client.delete(path=f"traffic-groups/{traffic_group_id}", body={})
