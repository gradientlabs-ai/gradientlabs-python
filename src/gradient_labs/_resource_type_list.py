from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_type import ResourceType


@dataclass_json
@dataclass(frozen=True)
class ResourceTypesList:
    """ResourceTypesList contains the list of resource types."""

    resource_types: List[ResourceType]


def list_resource_types(*, client: HttpClient) -> ResourceTypesList:
    """list_resource_types lists all resource types.

    Note: requires a Management API key.
    """
    rsp = client.get(path="resource-types", body={})
    return ResourceTypesList.from_dict(rsp)
