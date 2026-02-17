from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .secret import Secret, RefreshMechanismHTTP


@dataclass_json
@dataclass(frozen=True)
class WriteSecretParams:
    """WriteSecretParams contains the parameters for writing (creating or updating) a secret."""

    # name is the unique identifier for the secret.
    name: str

    # value is the secret value to store.
    value: str

    # expiry is the optional expiration time for the secret.
    expiry: Optional[datetime] = None

    # refresh_mechanism_http is the optional configuration for automatically refreshing
    # the secret value using an HTTP request (e.g., OAuth token refresh).
    refresh_mechanism_http: Optional[RefreshMechanismHTTP] = None


def write_secret(*, client: HttpClient, params: WriteSecretParams) -> Secret:
    """write_secret creates or updates a secret. If a secret with the given name already exists,
    it will be updated with the new value and configuration.

    Note: requires a `Management` API key."""
    # Build body manually to handle datetime serialization and exclude name from body
    body = {
        "value": params.value,
    }
    if params.expiry is not None:
        body["expiry"] = HttpClient.localize(params.expiry)
    if params.refresh_mechanism_http is not None:
        body["refresh_mechanism_http"] = params.refresh_mechanism_http.to_dict()

    rsp = client.put(path=f"secrets/{params.name}", body=body)
    return Secret.from_dict(rsp)
