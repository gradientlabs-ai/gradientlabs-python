from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_type import ResourceType, Scope, RefreshStrategy, SourceConfig


@dataclass_json
@dataclass(frozen=True)
class CreateResourceTypeParams:
    """CreateResourceTypeParams contains the parameters for creating a resource type."""

    # DisplayName is a human-readable name for the resource type.
    display_name: str

    # Scope determines when in the conversation the resource is fetched and used.
    scope: Scope

    # RefreshStrategy determines how often the resource is re-fetched.
    refresh_strategy: RefreshStrategy

    # Description is an optional human-readable description of the resource type.
    description: Optional[str] = None

    # SourceConfig defines how the resource is fetched.
    source_config: Optional[SourceConfig] = None

    # IsEnabled indicates whether the resource type should be enabled.
    is_enabled: Optional[bool] = None


def create_resource_type(
    *, client: HttpClient, params: CreateResourceTypeParams
) -> ResourceType:
    """create_resource_type creates a new resource type.

    Note: requires a Management API key.
    """
    body = {
        "display_name": params.display_name,
        "scope": params.scope.value,
        "refresh_strategy": params.refresh_strategy.value,
    }
    if params.description is not None:
        body["description"] = params.description
    if params.source_config is not None:
        body["source_config"] = params.source_config.to_dict()
    if params.is_enabled is not None:
        body["is_enabled"] = params.is_enabled

    rsp = client.post(path="resource-types", body=body)
    return ResourceType.from_dict(rsp)
