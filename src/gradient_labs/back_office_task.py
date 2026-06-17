from typing import Optional, Any, List
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


class BackOfficeTaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"
    HANDED_OFF = "handed-off"


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskResult:
    result_type: str
    custom: Optional[Any] = None


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskAttachment:
    idempotency_key: str
    file_name: str
    external_url: Optional[str] = None


# Reusable marshmallow config for optional datetime fields; avoids repeating allow_none/load_default.
_optional_datetime_config = config(
    encoder=lambda x: x.isoformat() if x is not None else None,
    decoder=lambda x: datetime.fromisoformat(x) if x is not None else None,
    mm_field=fields.DateTime(format="iso", allow_none=True, load_default=None),
)


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTask:
    id: str
    agent_id: str
    status: BackOfficeTaskStatus
    input: Any
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    metadata: Optional[Any] = None
    attachments: Optional[List[BackOfficeTaskAttachment]] = None
    updated: Optional[datetime] = field(
        default=None, metadata=_optional_datetime_config
    )
    completed: Optional[datetime] = field(
        default=None, metadata=_optional_datetime_config
    )
    failed: Optional[datetime] = field(default=None, metadata=_optional_datetime_config)
    failure_reasons: Optional[List[str]] = None
    handed_off: Optional[datetime] = field(
        default=None, metadata=_optional_datetime_config
    )
    hand_off_reason: Optional[str] = None
    result: Optional[BackOfficeTaskResult] = None
