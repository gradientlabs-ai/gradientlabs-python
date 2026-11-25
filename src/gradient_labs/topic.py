from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any

from dataclasses_json import dataclass_json, config

from ._datetime import datetime_config_named
from .article import Visibility


@dataclass_json
@dataclass(frozen=True)
class Topic:
    """Topic is an article topic. The API names its fields in CamelCase
    (e.g. `ExternalID`), so each field below says which one it reads."""

    # source is the support platform this topic comes from, such as "public-api"
    # or "intercom".
    source: str = field(metadata=config(field_name="Source"))

    # external_id is your identifier for this topic on the support platform.
    external_id: str = field(metadata=config(field_name="ExternalID"))

    # name is the topic's name.
    name: str = field(metadata=config(field_name="Name"))

    # visibility describes who can see this topic.
    visibility: Visibility = field(metadata=config(field_name="Visibility"))

    # created is when the topic was first created on the support platform.
    created: datetime = field(metadata=datetime_config_named("Created"))

    # last_edited is when the topic was last changed on the support platform.
    last_edited: datetime = field(metadata=datetime_config_named("LastEdited"))

    # last_seen is when Gradient Labs last saw this topic while syncing.
    last_seen: datetime = field(metadata=datetime_config_named("LastSeen"))

    # data is the topic as the support platform represents it, base64-encoded.
    data: Any = field(metadata=config(field_name="Data"))

    # description is a short description of the topic.
    description: Optional[str] = field(
        default=None, metadata=config(field_name="Description")
    )

    # parent_external_id identifies the topic this one sits under, if any.
    parent_external_id: Optional[str] = field(
        default=None, metadata=config(field_name="ParentExternalID")
    )

    # public_url is a link to the topic online, if it has one.
    public_url: Optional[str] = field(
        default=None, metadata=config(field_name="PublicURL")
    )
