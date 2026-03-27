from ._http_client import HttpClient


def unset_procedure_live_version(
    *, client: HttpClient, procedure_id: str, version: int
) -> None:
    """unset_procedure_live_version removes the specified version of a procedure from being the live revision.

    Once unset, the version will no longer be used by default by the agent.
    Unsetting the live version does not delete the version or affect the gated status (if any).

    Note: requires a `Management` API key."""
    client.post(
        path=f"procedures/{procedure_id}/versions/{version}/unset-live",
        body={},
    )
