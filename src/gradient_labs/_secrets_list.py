from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .secret import Secret
from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class SecretsList:
    """SecretsList contains the list of all secrets."""

    secrets: List[Secret]


def list_secrets(*, client: HttpClient) -> SecretsList:
    """list_secrets returns all of your secrets.

    Note: requires a `Management` API key."""
    rsp = client.get(
        path="secrets",
        body={},
    )
    return SecretsList.from_dict(rsp)
