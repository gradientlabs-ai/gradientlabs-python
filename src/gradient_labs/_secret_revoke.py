from ._http_client import HttpClient


def revoke_secret(*, client: HttpClient, name: str) -> None:
    """revoke_secret permanently deletes a secret. This action cannot be undone.

    Note: requires a `Management` API key."""
    _ = client.delete(path=f"secrets/{name}", body={})
