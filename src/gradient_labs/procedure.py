from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from ._datetime import parse_datetime


class ProcedureStatus(str, Enum):
    """Identifies the publication status of a procedure."""

    # DRAFT indicates the procedure has been saved as a draft, but
    # won't be used in real conversations until it is promoted to live.
    DRAFT: str = "draft"

    # LIVE indicates the procedure is live and will be used in real
    # conversations.
    LIVE: str = "live"

    # UNSAVED indicates the procedure has changes that have not been saved yet.
    UNSAVED: str = "unsaved"

    # ARCHIVED indicates the procedure has been archived.
    ARCHIVED: str = "archived"


@dataclass_json
@dataclass(frozen=True)
class Procedure:
    """A procedure and its publication status."""

    # id uniquely identifies the procedure.
    id: str

    # name is the user-given name of the procedure.
    name: str

    # status is the overall status of the procedure.
    status: ProcedureStatus

    # created is the time at which the procedure was originally created.
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # updated is the time at which the procedure's status, metadata, or current
    # revision was last changed. It does *not* reflect revisions created as part
    # of testing unsaved changes.
    updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # has_daily_limit is true if this procedure can only be executed for a maximum
    # number of conversations in a given day (defined below).
    has_daily_limit: bool

    # max_daily_conversations is the maximum number of conversations that a procedure
    # can be used in on a given day, when it is rate limited.
    max_daily_conversations: Optional[int] = None

    # description says when the procedure applies.
    description: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class GatedConfig:
    """Configuration for gated procedure versions."""

    # max_daily_conversations is the maximum number of conversations per day
    # that can use the gated version.
    max_daily_conversations: int = field(
        metadata=config(field_name="MaxDailyConversations")
    )


@dataclass_json
@dataclass(frozen=True)
class ProcedureVersion:
    """A specific version of a procedure."""

    # name is the user-given name of the procedure at the time of this version.
    name: str = field(metadata=config(field_name="Name"))

    # description of the procedure at the time of this version.
    description: str = field(metadata=config(field_name="Description"))

    # version is a numeric identifier for the version. It is incremented every
    # time a new version of the procedure is saved.
    version: int = field(metadata=config(field_name="Version"))

    # author is the ID of the user who created this version of the procedure.
    author: str = field(metadata=config(field_name="Author"))

    # created is the time at which this version of the procedure was created.
    created: datetime = field(
        metadata=config(
            field_name="Created",
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # gated indicates whether the version is a gated version that is used before "live",
    # within the daily limit defined in gated_config.
    gated: bool = field(metadata=config(field_name="Gated"))

    # gated_config defines how the gated version is limited.
    # gated_config is relevant only if gated == True.
    gated_config: Optional[GatedConfig] = field(
        metadata=config(field_name="GatedConfig")
    )

    # live indicates whether the version is the "production" version used by the agent by default,
    # if there are no gated versions or all gated versions have exceeded their limit.
    live: bool = field(metadata=config(field_name="Live"))
