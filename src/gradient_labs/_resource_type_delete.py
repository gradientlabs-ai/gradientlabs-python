from ._http_client import HttpClient


def delete_resource_type(*, client: HttpClient, id: str) -> None:
    """delete_resource_type deletes a resource type by ID.

    Note: requires a Management API key.
    """
    _ = client.delete(path=f"resource-types/{id}", body={})
