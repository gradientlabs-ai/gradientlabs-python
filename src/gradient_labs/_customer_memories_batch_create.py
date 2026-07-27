from typing import Optional, List, Dict, Any
from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class CustomerMemory:
    # external_id is your own identifier for this memory.
    external_id: str

    # created_at is when the event this memory describes occurred.
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # data is an arbitrary JSON object stored verbatim as the memory's payload.
    data: Dict[str, Any]

    # custom_type is an optional free-form label for the memory.
    custom_type: Optional[str] = None


def batch_create_customer_memories(
    *, client: HttpClient, customer_id: str, memories: List[CustomerMemory]
) -> None:
    """batch_create_customer_memories stores a batch of memories scoped to a
    customer, for the AI agent to search over on demand.

    Each memory's data is stored verbatim as an arbitrary JSON object. The call
    is asynchronous: it returns as soon as the batch is accepted. It returns a
    409 Conflict if a batch is already being created for the same customer."""
    body: Dict[str, Any] = {
        "memories": [_memory_to_dict(memory) for memory in memories],
    }
    _ = client.post(
        path=f"customers/{customer_id}/memories",
        body=body,
    )


def _memory_to_dict(memory: CustomerMemory) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "external_id": memory.external_id,
        "created_at": HttpClient.localize(memory.created_at),
        "data": memory.data,
    }
    if memory.custom_type is not None:
        item["custom_type"] = memory.custom_type
    return item
