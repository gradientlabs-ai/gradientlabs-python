from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .note import Note


@dataclass_json
@dataclass(frozen=True)
class CreateNoteParams:
    """CreateNoteParams contains the parameters for creating a note."""

    # ID is your identifier for this note.
    id: str

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

    # Attributes says which customers the note applies to, as a map from attribute key
    # to the attribute values it applies to. The keys and values must match the
    # attributes defined for your company. Leave it out for a note that applies to
    # every conversation.
    attributes: Optional[Dict[str, List[str]]] = None

    # knowledge_base_ids optionally names the knowledge bases this note belongs to. The
    # list cannot be empty. If you leave it out, the note goes into the default
    # "public-api" knowledge base.
    knowledge_base_ids: Optional[List[str]] = None


def create_note(*, client: HttpClient, params: CreateNoteParams) -> Note:
    """create_note creates a new note."""
    body = {
        "id": params.id,
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
    if params.attributes is not None:
        body["attributes"] = params.attributes
    if params.knowledge_base_ids is not None:
        body["knowledge_base_ids"] = params.knowledge_base_ids

    rsp = client.post(path="notes", body=body)
    return Note.from_dict(rsp)
