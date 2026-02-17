from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from dataclasses_json import dataclass_json

from .article import Visibility


@dataclass_json
@dataclass(frozen=True)
class Topic:
    """Topic represents an article topic for categorizing help articles."""

    # source identifies the CRM or support platform that the topic comes from
    source: str

    # external_id identifies this topic in the Source
    external_id: str

    # name is the human-readable name for this topic
    name: str

    # visibility describes who can see the topic
    visibility: Visibility

    # created is when the topic was created in the source
    created: datetime

    # last_edited is when the topic was last changed in the source
    last_edited: datetime

    # last_seen is the last time we saw this topic when crawling
    last_seen: datetime

    # data is a raw representation of the topic from the support platform
    data: Any

    # description is the optional subtext for the topic
    description: Optional[str] = None

    # parent_external_id identifies the topic that this topic is nested under
    parent_external_id: Optional[str] = None

    # public_url optionally points to the public resource for this topic
    public_url: Optional[str] = None
