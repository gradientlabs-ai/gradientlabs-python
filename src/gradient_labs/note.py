from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

from ._datetime import optional_datetime_config


class NoteStatus(str, Enum):
    """NoteStatus describes whether a note is draft, live, or deleted."""

    # DRAFT means the note is being written or edited and is not published.
    DRAFT: str = "draft"

    # LIVE means the note is published and available.
    LIVE: str = "live"

    # DELETED means the note has been deleted.
    DELETED: str = "deleted"


@dataclass_json
@dataclass
class Note:
    """Note represents a note in the Gradient Labs system."""

    # ID is the internal Gradient Labs ID for this note.
    gradient_labs_id: str

    # ExternalID is your identifier for this note.
    id: str

    # Title is the note's title.
    title: str

    # Body is the main contents of the note.
    body: Optional[str] = None

    # WebpageURL optionally points to a webpage to use as the note body.
    url: Optional[str] = None

    # StartTime is when the note becomes relevant.
    valid_from: Optional[datetime] = field(
        default=None, metadata=optional_datetime_config
    )

    # EndTime is when the note is no longer relevant.
    valid_to: Optional[datetime] = field(
        default=None, metadata=optional_datetime_config
    )

    # LastModifiedBy identifies who last modified the note.
    last_modified_by: str = ""

    # Created is when the note was created.
    created: Optional[datetime] = field(default=None, metadata=optional_datetime_config)

    # Updated is when the note was last updated.
    updated: Optional[datetime] = field(default=None, metadata=optional_datetime_config)

    # Status describes whether the note is draft, live, or deleted.
    status: NoteStatus = NoteStatus.DRAFT

    # Attributes says which customers the note applies to, as a map from attribute key
    # to the attribute values it applies to. Empty means every conversation.
    attributes: Optional[Dict[str, List[str]]] = None
