from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime


class SourceType(str, Enum):
    """SourceType describes how the data is fetched from the source."""

    # HTTP means the source fetches data via HTTP requests.
    HTTP: str = "http"

    # INTERNAL means the source is provided by the system.
    INTERNAL: str = "internal"

    # WEBHOOK means the source receives data via webhooks.
    WEBHOOK: str = "webhook"


class SchemaUpdateStrategy(str, Enum):
    """SchemaUpdateStrategy represents how the new schema should be applied."""

    # MERGE merges the inferred schema with the existing schema, preserving existing fields and adding new ones.
    MERGE: str = "merge"

    # REPLACE completely replaces the existing schema with the newly inferred one.
    REPLACE: str = "replace"


@dataclass_json
@dataclass(frozen=True)
class ResourceHTTPBodyDefinition:
    """ResourceHTTPBodyDefinition determines how the HTTP request body is constructed."""

    # Encoding determines how the HTTP request body will be encoded.
    encoding: str

    # JSONTemplate contains a template that will be used to generate JSON for the HTTP request body.
    # Only used when Encoding is "application/json".
    json_template: Optional[str] = None

    # FormFieldTemplates contains templates for the values that will be form-encoded and used as the HTTP body.
    # Only used when Encoding is "application/x-www-form-urlencoded".
    form_field_templates: Optional[Dict[str, str]] = None


@dataclass_json
@dataclass(frozen=True)
class ResourceHTTPDefinition:
    """ResourceHTTPDefinition contains configuration for HTTP actions."""

    # Method is the HTTP request method that will be used.
    method: str

    # URLTemplate contains a template used to construct the request URL.
    url_template: str

    # HeaderTemplates contains templates for the values that will be used as request headers.
    header_templates: Optional[Dict[str, str]] = None

    # Body determines how the HTTP request body is constructed.
    body: Optional[ResourceHTTPBodyDefinition] = None


@dataclass_json
@dataclass(frozen=True)
class ResourceWebhookDefinition:
    """ResourceWebhookDefinition contains configuration for webhook actions."""

    # Name will be included in the `data.action` field of the webhook payload.
    name: str


@dataclass_json
@dataclass
class ResourceSource:
    """ResourceSource represents a resource source in the system."""

    # ID is a generated ID for the resource source.
    id: str

    # DisplayName free-text field to describe the source, eg. "Intercom User Attributes".
    # Enforced unique per company.
    display_name: str

    # SourceType describes how the data is fetched from the source.
    source_type: SourceType

    # Created is the timestamp when the resource source was created.
    created: datetime

    # Updated is the timestamp when the resource source was last updated.
    updated: datetime

    # Description optional free-text field to describe the source in more detail.
    description: Optional[str] = None

    # HTTPConfig can be set up by customers.
    http_config: Optional[ResourceHTTPDefinition] = None

    # WebhookConfig can be set up by customers.
    webhook_config: Optional[ResourceWebhookDefinition] = None

    # AttributeDescriptions optional raw attribute-level descriptions, used when generating the schema
    # and as additional information for the agent.
    # - key: a JSONPath eg. `$.name` or `$.items[*].name`
    # - value: a description of the attribute
    attribute_descriptions: Optional[Dict[str, str]] = None

    # Schema is the schema of the resource source, inferred from the source payloads.
    # It is updated asynchronously as data is fetched from the source.
    # Nil if the schema has not been inferred yet. Includes attribute descriptions if present.
    schema: Optional[Any] = None
