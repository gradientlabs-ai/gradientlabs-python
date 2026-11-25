from typing import Any


def without_none(value: Any) -> Any:
    """without_none drops None values from nested dicts and lists, so that unset
    optional fields are left out of a request instead of sent as null."""
    if isinstance(value, dict):
        return {k: without_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [without_none(v) for v in value]
    return value
