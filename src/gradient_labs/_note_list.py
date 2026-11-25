from typing import List, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from ._pagination import ForwardPaginationInfo
from .note import Note


@dataclass_json
@dataclass(frozen=True)
class NoteListParams:
    """NoteListParams contains the parameters for listing notes."""

    # cursor is the page to fetch, from `pagination.next` in a previous response.
    # Leave it out to get the first page.
    cursor: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class NoteListResponse:
    """NoteListResponse is a page of notes."""

    # notes are the notes on this page.
    notes: List[Note]

    # pagination contains the cursor for the next page, if there is one.
    pagination: ForwardPaginationInfo


def list_notes(
    *, client: HttpClient, params: Optional[NoteListParams] = None
) -> NoteListResponse:
    """list_notes returns a page of the notes created by your company.

    Note: requires a `Management` API key."""
    query_params = {}
    if params is not None and params.cursor is not None:
        query_params["cursor"] = params.cursor

    rsp = client.get(path="notes", query_params=query_params)
    return NoteListResponse.from_dict(rsp)
