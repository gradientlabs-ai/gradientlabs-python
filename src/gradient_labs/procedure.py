from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


class ProcedureStatus(str, Enum):
    """Identifies the publication status of a procedure."""

    # DRAFT indicates the procedure has been saved as a draft, but
    # won't be used in real conversations until it is promoted to live.
    DRAFT: str = "draft"

    # LIVE indicates the procedure is live and will be used in real
    # conversations.
    LIVE: str = "live"


@dataclass_json
@dataclass(frozen=True)
class UserDetails:
    """UserDetails describes a procedure author."""

    email: str


@dataclass_json
@dataclass(frozen=True)
class Procedure:
    """UserDetails describes a procedure author."""

    # id uniquely identifies the procedure.
    id: str

    # name is the user-given name of the procedure.
    name: str

    # status is the overall status of the procedure.
    status: ProcedureStatus

    # author is the user who originally created the procedure.
    author: UserDetails

    # created is the time at which the procedure was originally created.
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # updated is the time at which the procedure's status, metadata, or current
    # revision was last changed. It does *not* reflect revisions created as part
    # of testing unsaved changes.
    updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # has_daily_limit is true if this procedure can only be executed for a maximum
    # number of conversations in a given day (defined below).
    has_daily_limit: bool

    # max_daily_conversations is the maximum number of conversations that a procedure
    # can be used in on a given day, when it is rate limited.
    max_daily_conversations: int


@dataclass_json
@dataclass(frozen=True)
class ExperimentalConfig:
    """Configuration for experimental procedure versions."""

    # max_daily_conversations is the maximum number of conversations per day
    # that can use this experimental version.
    max_daily_conversations: int


@dataclass_json
@dataclass(frozen=True)
class ProcedureVersion:
    """A specific version of a procedure."""

    # name is the user-given name of the procedure at the time of this version.
    name: str

    # description of the procedure at the time of this version.
    description: str

    # version is a numeric identifier for the version. It is incremented every
    # time a new version of the procedure is saved.
    version: int

    # author is the ID of the user who created this version of the procedure.
    author: str

    # created is the time at which this version of the procedure was created.
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # experimental indicates whether this is an experimental version that is used before "live",
    # within the daily limit defined in experimental_config.
    experimental: bool

    # experimental_config defines how the experimental version is limited.
    # Relevant only if experimental == True.
    experimental_config: ExperimentalConfig | None

    # live indicates whether this is the "production" version that is used by the agent by default,
    # if there are no experimental versions or all of them have exceeded their limit.
    live: bool
