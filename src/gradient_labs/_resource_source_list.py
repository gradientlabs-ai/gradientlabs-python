from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_source import ResourceSource


@dataclass_json
@dataclass(frozen=True)
class ResourceSourcesList:
    """ResourceSourcesList contains a list of resource sources."""

    resource_sources: List[ResourceSource]


def list_resource_sources(*, client: HttpClient) -> ResourceSourcesList:
    """list_resource_sources lists all resource sources.

    Note: requires a Management API key.
    """
    rsp = client.get(path="resource-sources", body={})
    return ResourceSourcesList.from_dict(rsp)
