from ._http_client import HttpClient


def set_procedure_live_version(
    *, client: HttpClient, procedure_id: str, version: int
) -> None:
    """set_procedure_live_version promotes a specific version of a procedure to be the
    live (production) version that the AI agent will use for new conversations.

    The live version is the default version used by the agent when no experimental
    versions are active. If the specified version is currently marked as experimental,
    it will be promoted to live and will no longer be considered experimental.

    This is typically used after testing a procedure version in experimental mode
    and confirming it works correctly. Once live, the procedure version will be
    used for all new conversations that match the procedure's criteria.

    Note: requires a `Management` API key."""
    client.post(
        path=f"procedures/{procedure_id}/versions/{version}/set-live",
        body={},
    )
