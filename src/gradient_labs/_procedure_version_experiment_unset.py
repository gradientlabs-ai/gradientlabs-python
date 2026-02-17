from ._http_client import HttpClient


def unset_procedure_experiment_version(
    *, client: HttpClient, procedure_id: str, version: int
) -> None:
    """unset_procedure_experiment_version removes the specified version of a procedure from being
    marked as experimental.

    Once unset, the version will no longer be used for A/B testing or served as an experiment.

    Note: requires a `Management` API key."""
    client.post(
        path=f"procedures/{procedure_id}/versions/{version}/unset-experiment",
        body={},
    )
