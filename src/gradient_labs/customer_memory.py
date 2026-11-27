from typing import Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ._datetime import datetime_config


@dataclass_json
@dataclass(frozen=True)
class CustomerMemoryType:
    """CustomerMemoryType is the customer-defined category of a memory."""

    # name is the name of the category. `support_conversation` is reserved for Gradient Labs.
    name: str

    # description is an optional description of the category.
    description: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class CustomerMemory:
    """CustomerMemory is something remembered about a customer."""

    # external_id is your own identifier for the memory.
    external_id: str

    # custom_type is the category of the memory.
    custom_type: CustomerMemoryType

    # created_at is when the memory's underlying event occurred.
    created_at: datetime = field(metadata=datetime_config)

    # data is the memory's payload, any JSON value.
    data: Any


@dataclass_json
@dataclass(frozen=True)
class CustomerMemoriesList:
    """CustomerMemoriesList contains all memories retained for a customer."""

    memories: List[CustomerMemory]
