from typing import Optional, Dict, Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_source import (
    ResourceSource,
    SourceType,
    ResourceHTTPDefinition,
    ResourceWebhookDefinition,
)


@dataclass_json
@dataclass(frozen=True)
class UpdateResourceSourceParams:
    """UpdateResourceSourceParams contains the parameters for updating a resource source.

    All fields are optional. If a field is not provided, its value will not be changed.
    """

    # DisplayName is a human-readable name for the resource source.
    display_name: Optional[str] = None

    # Description is an optional human-readable description of the resource source.
    description: Optional[str] = None

    # SourceType describes how the data is fetched from the source.
    # Note: source_type cannot be updated once set. To change the source_type, you must create a new resource source.
    source_type: Optional[SourceType] = None

    # HTTPConfig can be set up by customers.
    # When updating http_config, the entire object must be provided.
    http_config: Optional[ResourceHTTPDefinition] = None

    # WebhookConfig can be set up by customers.
    # When updating webhook_config, the entire object must be provided.
    webhook_config: Optional[ResourceWebhookDefinition] = None

    # AttributeDescriptions optional raw attribute-level descriptions.
    attribute_descriptions: Optional[Dict[str, str]] = None

    # Schema is the schema of the resource source.
    schema: Optional[Any] = None


def update_resource_source(
    *, client: HttpClient, id: str, params: UpdateResourceSourceParams
) -> ResourceSource:
    """update_resource_source updates an existing resource source.

    Note: requires a Management API key.
    """
    body = {}
    if params.display_name is not None:
        body["display_name"] = params.display_name
    if params.description is not None:
        body["description"] = params.description
    if params.source_type is not None:
        body["source_type"] = params.source_type.value
    if params.http_config is not None:
        body["http_config"] = params.http_config.to_dict()
    if params.webhook_config is not None:
        body["webhook_config"] = params.webhook_config.to_dict()
    if params.attribute_descriptions is not None:
        body["attribute_descriptions"] = params.attribute_descriptions
    if params.schema is not None:
        body["schema"] = params.schema

    rsp = client.put(path=f"resource-sources/{id}", body=body)
    return ResourceSource.from_dict(rsp)
