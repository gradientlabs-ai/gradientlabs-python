from ._http_client import HttpClient
from .resource_source import ResourceSource


def read_resource_source(*, client: HttpClient, id: str) -> ResourceSource:
    """read_resource_source reads a specific resource source by ID.

    Note: requires a Management API key.
    """
    rsp = client.get(path=f"resource-sources/{id}", body={})
    return ResourceSource.from_dict(rsp)
