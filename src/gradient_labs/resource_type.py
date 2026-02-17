from typing import Optional, List, Any
from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime


class Scope(str, Enum):
    """Scope determines when in the conversation the resource is fetched and used."""

    # GLOBAL means the resource is available throughout the conversation and in all procedures.
    GLOBAL: str = "global"

    # LOCAL means the resource is available only in procedures that explicitly use it, only fetched when it's used.
    LOCAL: str = "local"


class RefreshStrategy(str, Enum):
    """RefreshStrategy determines how often the resource is re-fetched."""

    # DYNAMIC means the resource value can change, so this is re-fetched throughout the conversation.
    DYNAMIC: str = "dynamic"

    # STATIC means the resource is fetched once at the start of the conversation (global) or when it's first used in a procedure (local).
    STATIC: str = "static"


@dataclass_json
@dataclass(frozen=True)
class SourceConfig:
    """SourceConfig defines how the resource is fetched."""

    # SourceID identifies the source which should be used to fetch the resource data.
    source_id: str

    # Attributes defines the top-level field names to be used from the source data.
    attributes: Optional[List[str]] = None

    # Cache determines how long we'll consider data from the source be valid before refreshing it.
    # It's either a duration string (e.g. "5m") or "never" if the resource is refreshed on every turn.
    # The default is 1 minute.
    cache: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class Attribute:
    """Attribute describes a single attribute in the resource schema."""

    # Path is the JSON path to the attribute (e.g., "user.name", "orderDetails[0].item").
    path: str

    # Type is the data type of the attribute (e.g., "string", "number", "integer", "boolean", "object", "array").
    type: str

    # Cardinality is whether the attribute can have one value ("one") or multiple values ("many").
    cardinality: str

    # Name is the name of the attribute (the last part of the path).
    name: str

    # Description is an optional description of the attribute.
    description: Optional[str] = None

    # IsRoot indicates whether the attribute is a top-level field in the resource data.
    is_root: Optional[bool] = None


@dataclass_json
@dataclass(frozen=True)
class Schema:
    """Schema describes the structure of the resource data."""

    # Raw is the raw JSON schema for the resource data.
    raw: Optional[Any] = None

    # Attributes is an array of attribute descriptors for the resource data.
    attributes: Optional[List[Attribute]] = None


@dataclass_json
@dataclass
class ResourceType:
    """ResourceType represents a resource type configuration."""

    # ID is the unique identifier for the resource type.
    id: str

    # DisplayName is a human-readable name for the resource type.
    display_name: str

    # Description is an optional human-readable description of the resource type.
    description: Optional[str] = None

    # Scope determines when in the conversation the resource is fetched and used.
    scope: Scope = Scope.GLOBAL

    # RefreshStrategy determines how often the resource is re-fetched.
    refresh_strategy: RefreshStrategy = RefreshStrategy.DYNAMIC

    # SourceConfig defines how the resource is fetched.
    source_config: Optional[SourceConfig] = None

    # Schema describes the structure of the data returned by the resource source.
    schema: Optional[Schema] = None

    # IsEnabled indicates whether the resource type is enabled.
    is_enabled: bool = False

    # Created is when the resource type was created.
    created: Optional[datetime] = None

    # Updated is when the resource type was last updated.
    updated: Optional[datetime] = None
