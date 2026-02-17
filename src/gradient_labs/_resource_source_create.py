from typing import Optional, Dict
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
class CreateResourceSourceParams:
    """CreateResourceSourceParams contains the parameters for creating a resource source."""

    # DisplayName is a human-readable name for the resource source.
    display_name: str

    # SourceType describes how the data is fetched from the source.
    source_type: SourceType

    # Description is an optional human-readable description of the resource source.
    description: Optional[str] = None

    # HTTPConfig can be set up by customers. Required if source_type is HTTP.
    http_config: Optional[ResourceHTTPDefinition] = None

    # WebhookConfig can be set up by customers. Required if source_type is WEBHOOK.
    webhook_config: Optional[ResourceWebhookDefinition] = None

    # AttributeDescriptions optional raw attribute-level descriptions.
    attribute_descriptions: Optional[Dict[str, str]] = None


def create_resource_source(
    *, client: HttpClient, params: CreateResourceSourceParams
) -> ResourceSource:
    """create_resource_source creates a new resource source.

    Note: requires a Management API key.
    """
    body = {
        "display_name": params.display_name,
        "source_type": params.source_type.value,
    }
    if params.description is not None:
        body["description"] = params.description
    if params.http_config is not None:
        body["http_config"] = params.http_config.to_dict()
    if params.webhook_config is not None:
        body["webhook_config"] = params.webhook_config.to_dict()
    if params.attribute_descriptions is not None:
        body["attribute_descriptions"] = params.attribute_descriptions

    rsp = client.post(path="resource-sources", body=body)
    return ResourceSource.from_dict(rsp)
