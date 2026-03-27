from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class SetProcedureGatedVersionParams:
    """Parameters for setting a gated version of a procedure.

    Gated versions allow gradual rollout of new procedure versions
    with daily conversation limits."""

    # max_daily_conversations limits how many conversations per day can use the gated version.
    # max_daily_conversations allows gradual rollout of a new procedure version.
    max_daily_conversations: int

    # replace: if True, an existing gated version (if any) will be replaced with a new one.
    # Otherwise, if another gated version already exists, an error will be returned.
    replace: bool = False


def set_procedure_gated_version(
    *,
    client: HttpClient,
    procedure_id: str,
    version: int,
    params: SetProcedureGatedVersionParams,
) -> None:
    """set_procedure_gated_version marks the specified procedure version as gated.

    Gated versions are used for A/B testing and are served to a limited number
    of conversations per day. If a gated version already exists, the gated version
    will only be replaced if the 'replace' flag is set to True.

    Note: requires a `Management` API key."""
    body = {
        "max_daily_conversations": params.max_daily_conversations,
        "replace": params.replace,
    }
    client.post(
        path=f"procedures/{procedure_id}/versions/{version}/set-gated",
        body=body,
    )
