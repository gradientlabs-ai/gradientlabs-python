from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .procedure import ProcedureVersion


@dataclass_json
@dataclass(frozen=True)
class ListProcedureVersionsResponse:
    """Response containing list of procedure versions."""

    versions: List[ProcedureVersion]


def list_procedure_versions(
    *, client: HttpClient, procedure_id: str
) -> ListProcedureVersionsResponse:
    """list_procedure_versions lists existing non-ephemeral versions of a procedure.

    Note: requires a `Management` API key."""
    body = client.get(
        path=f"procedures/{procedure_id}/versions",
        body={},
    )
    return ListProcedureVersionsResponse.from_dict(body)
