from typing import Any, List
from datetime import datetime
from dataclasses import dataclass

from ._http_client import HttpClient
from .customer_memory import CustomerMemoryType


@dataclass(frozen=True)
class BatchCreateCustomerMemory:
    """BatchCreateCustomerMemory is one memory to store about a customer."""

    # external_id is your own identifier for the memory. It must be unique within
    # your company. Retrying the same memory is safe and creates no duplicate.
    external_id: str

    # custom_type is the category of the memory.
    custom_type: CustomerMemoryType

    # created_at is when the memory's underlying event occurred.
    created_at: datetime

    # data is any JSON value as the memory's payload.
    data: Any


@dataclass(frozen=True)
class BatchCreateCustomerMemoriesParams:
    """BatchCreateCustomerMemoriesParams contains the memories to store."""

    memories: List[BatchCreateCustomerMemory]


def batch_create_customer_memories_v2(
    *,
    client: HttpClient,
    customer_id: str,
    params: BatchCreateCustomerMemoriesParams,
) -> None:
    """batch_create_customer_memories_v2 stores memories about a customer.

    Note: requires an `Integration` API key."""
    body = {
        "memories": [
            {
                "external_id": m.external_id,
                "custom_type": {
                    k: v for k, v in m.custom_type.to_dict().items() if v is not None
                },
                "created_at": HttpClient.localize(m.created_at),
                "data": m.data,
            }
            for m in params.memories
        ]
    }
    _ = client.post(path=f"customers/{customer_id}/memories/v2", body=body)
