from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


@dataclass_json
@dataclass(frozen=True)
class TerminologySubstitution:
    id: str
    blocked: str
    blocked_description: str
    replacement: str
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    resource_type_id: Optional[str] = None
    resource_attribute_json_path: Optional[str] = None
    resource_value_to_match: Optional[str] = None
