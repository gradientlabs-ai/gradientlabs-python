from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

from ._datetime import datetime_config, optional_datetime_config
from .tool import HTTPDefinition


@dataclass_json
@dataclass(frozen=True)
class SecretHTTPRetry:
    request_timeout_seconds: Optional[int] = None


@dataclass_json
@dataclass(frozen=True)
class SecretHTTPRequest(HTTPDefinition):
    retry: Optional[SecretHTTPRetry] = None


@dataclass_json
@dataclass(frozen=True)
class RefreshMechanismHTTP:
    """RefreshMechanismHTTP defines how to automatically refresh a secret's value
    using an HTTP request. This is commonly used for OAuth access tokens that
    need periodic renewal."""

    # request_definition specifies the HTTP request to make to refresh the secret.
    request_definition: SecretHTTPRequest

    # response_param_name is the JSON field name in the response that contains
    # the new secret value.
    response_param_name: str


@dataclass_json
@dataclass
class Secret:
    """Secret represents a stored secret with optional expiration and refresh configuration."""

    # name is the unique identifier for the secret.
    name: str

    # created is when the secret was first created.
    created: datetime = field(metadata=datetime_config)

    # updated is when the secret was last updated.
    updated: datetime = field(metadata=datetime_config)

    # expiry is the optional expiration time for the secret.
    expiry: Optional[datetime] = field(default=None, metadata=optional_datetime_config)

    # refresh_mechanism_http is the optional configuration for automatically refreshing
    # the secret value using an HTTP request (e.g., OAuth token refresh).
    refresh_mechanism_http: Optional[RefreshMechanismHTTP] = None
