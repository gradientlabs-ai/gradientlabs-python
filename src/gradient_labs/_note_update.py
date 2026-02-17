from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .note import Note


@dataclass_json
@dataclass(frozen=True)
class UpdateNoteParams:
    """UpdateNoteParams contains the parameters for updating a note."""

    # Title is the note's title.
    title: str

    # Body is the main contents of a note. This is mutually exclusive with webpage_url.
    body: Optional[str] = None

    # WebpageURL optionally points to a webpage to use as the note body.
    # This is mutually exclusive with body.
    webpage_url: Optional[str] = None

    # StartTime is when the note becomes relevant.
    start_time: Optional[datetime] = None

    # EndTime is when the note is no longer relevant.
    end_time: Optional[datetime] = None


def update_note(*, client: HttpClient, note_id: str, params: UpdateNoteParams) -> Note:
    """update_note updates an existing note's contents."""
    body = {
        "title": params.title,
    }
    if params.body is not None:
        body["body"] = params.body
    if params.webpage_url is not None:
        body["webpage_url"] = params.webpage_url
    if params.start_time is not None:
        body["start_time"] = HttpClient.localize(params.start_time)
    if params.end_time is not None:
        body["end_time"] = HttpClient.localize(params.end_time)

    rsp = client.post(path=f"notes/{note_id}", body=body)
    return Note.from_dict(rsp)
