from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json, config

from ._http_client import HttpClient
from .procedure import ProcedureVersion


@dataclass_json
@dataclass(frozen=True)
class ListProcedureVersionsResponse:
    """Response containing list of procedure versions."""

    # The API names this field `Versions`.
    versions: List[ProcedureVersion] = field(metadata=config(field_name="Versions"))


def list_procedure_versions(
    *, client: HttpClient, procedure_id: str
) -> ListProcedureVersionsResponse:
    """list_procedure_versions lists existing non-ephemeral versions of a procedure.

    Note: requires a `Management` API key."""
    body = client.get(path=f"procedures/{procedure_id}/versions")
    return ListProcedureVersionsResponse.from_dict(body)
