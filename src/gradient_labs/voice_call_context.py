from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from ._datetime import parse_datetime


@dataclass_json
@dataclass(frozen=True)
class VoiceCallContext:
    started_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    summary: Optional[str] = None
    transcript: Optional[str] = None
    handoff_reason: Optional[str] = None
    last_executed_procedure: Optional[str] = None
    last_executed_procedure_url: Optional[str] = None
    gradient_labs_url: Optional[str] = None
    live_handoff_url: Optional[str] = None
