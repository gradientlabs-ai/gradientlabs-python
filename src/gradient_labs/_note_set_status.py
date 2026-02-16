from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .note import NoteStatus


@dataclass_json
@dataclass(frozen=True)
class SetNoteStatusParams:
    """SetNoteStatusParams contains the parameters for setting a note's status."""

    # Status describes whether the note is draft, live, or deleted.
    status: NoteStatus


def set_note_status(
    *, client: HttpClient, note_id: str, params: SetNoteStatusParams
) -> None:
    """set_note_status updates a note's status."""
    _ = client.post(path=f"notes/{note_id}/status", body=params.to_dict())
