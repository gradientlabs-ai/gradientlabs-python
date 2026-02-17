from ._http_client import HttpClient
from .resource_type import ResourceType


def read_resource_type(*, client: HttpClient, id: str) -> ResourceType:
    """read_resource_type retrieves a specific resource type by ID.

    Note: requires a Management API key.
    """
    rsp = client.get(path=f"resource-types/{id}", body={})
    return ResourceType.from_dict(rsp)
