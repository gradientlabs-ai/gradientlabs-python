from ._http_client import HttpClient
from .note import Note


def read_note(*, client: HttpClient, note_id: str) -> Note:
    """read_note retrieves a note by your own ID for it.

    Note: requires a `Management` API key."""
    rsp = client.get(path=f"notes/{note_id}")
    return Note.from_dict(rsp)
