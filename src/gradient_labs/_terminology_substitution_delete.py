from ._http_client import HttpClient


def delete_terminology_substitution(
    *, client: HttpClient, substitution_id: str
) -> None:
    client.delete(path=f"terminology-substitutions/{substitution_id}", body={})
