from ._http_client import HttpClient


def delete_note(*, client: HttpClient, note_id: str) -> None:
    """delete_note marks a note as deleted."""
    _ = client.delete(path=f"notes/{note_id}", body={})
