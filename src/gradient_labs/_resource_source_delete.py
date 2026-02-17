from ._http_client import HttpClient


def delete_resource_source(*, client: HttpClient, id: str) -> None:
    """delete_resource_source deletes a resource source.

    Note: requires a Management API key.
    """
    _ = client.delete(path=f"resource-sources/{id}", body={})
