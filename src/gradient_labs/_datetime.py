import re
from datetime import datetime
from typing import Optional

from dataclasses_json import config
from marshmallow import fields


def parse_datetime(value: str) -> datetime:
    """parse_datetime reads an RFC 3339 timestamp, including a trailing `Z`."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    # Python 3.9 and 3.10 accept only three or six fractional digits.
    value = re.sub(
        r"(?<=:\d{2})\.(\d+)", lambda m: "." + m[1][:6].ljust(6, "0"), value, count=1
    )
    return datetime.fromisoformat(value)


def _parse_optional(value: Optional[str]) -> Optional[datetime]:
    return parse_datetime(value) if value is not None else None


def _format_optional(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value is not None else None


# datetime_config decodes a required RFC 3339 timestamp field.
datetime_config = config(
    encoder=datetime.isoformat,
    decoder=parse_datetime,
    mm_field=fields.DateTime(format="iso"),
)

# optional_datetime_config decodes an RFC 3339 timestamp field that may be absent or null.
optional_datetime_config = config(
    encoder=_format_optional,
    decoder=_parse_optional,
    mm_field=fields.DateTime(format="iso", allow_none=True, load_default=None),
)


def datetime_config_named(field_name: str) -> dict:
    """datetime_config_named is datetime_config for a field the API names differently."""
    return config(
        field_name=field_name,
        encoder=datetime.isoformat,
        decoder=parse_datetime,
        mm_field=fields.DateTime(format="iso"),
    )
