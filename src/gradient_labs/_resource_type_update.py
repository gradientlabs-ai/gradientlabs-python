from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_type import ResourceType, Scope, RefreshStrategy, SourceConfig


@dataclass_json
@dataclass(frozen=True)
class UpdateResourceTypeParams:
    """UpdateResourceTypeParams contains the parameters for updating a resource type."""

    # DisplayName is a human-readable name for the resource type.
    display_name: Optional[str] = None

    # Description is an optional human-readable description of the resource type.
    description: Optional[str] = None

    # Scope determines when in the conversation the resource is fetched and used.
    scope: Optional[Scope] = None

    # RefreshStrategy determines how often the resource is re-fetched.
    refresh_strategy: Optional[RefreshStrategy] = None

    # SourceConfig defines how the resource is fetched.
    source_config: Optional[SourceConfig] = None

    # IsEnabled indicates whether the resource type should be enabled.
    is_enabled: Optional[bool] = None


def update_resource_type(
    *, client: HttpClient, id: str, params: UpdateResourceTypeParams
) -> ResourceType:
    """update_resource_type updates an existing resource type.

    Note: requires a Management API key.
    """
    body = {}
    if params.display_name is not None:
        body["display_name"] = params.display_name
    if params.description is not None:
        body["description"] = params.description
    if params.scope is not None:
        body["scope"] = params.scope.value
    if params.refresh_strategy is not None:
        body["refresh_strategy"] = params.refresh_strategy.value
    if params.source_config is not None:
        body["source_config"] = params.source_config.to_dict()
    if params.is_enabled is not None:
        body["is_enabled"] = params.is_enabled

    rsp = client.put(path=f"resource-types/{id}", body=body)
    return ResourceType.from_dict(rsp)
