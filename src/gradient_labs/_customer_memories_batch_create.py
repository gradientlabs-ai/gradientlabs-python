from typing import Any, List
from datetime import datetime
from dataclasses import dataclass

from ._http_client import HttpClient


@dataclass(frozen=True)
class BatchCreateCustomerMemoryDeprecated:
    """BatchCreateCustomerMemoryDeprecated is one memory to store about a customer."""

    # external_id is your own identifier for the memory.
    external_id: str

    # custom_type is the name of the memory's category.
    custom_type: str

    # created_at is when the memory's underlying event occurred.
    created_at: datetime

    # data is any JSON value as the memory's payload.
    data: Any


@dataclass(frozen=True)
class BatchCreateCustomerMemoriesDeprecatedParams:
    """BatchCreateCustomerMemoriesDeprecatedParams contains the memories to store."""

    memories: List[BatchCreateCustomerMemoryDeprecated]


def batch_create_customer_memories(
    *,
    client: HttpClient,
    customer_id: str,
    params: BatchCreateCustomerMemoriesDeprecatedParams,
) -> None:
    """batch_create_customer_memories stores memories about a customer through the
    deprecated `POST /customers/{customer_id}/memories` endpoint. Use
    batch_create_customer_memories_v2 instead.

    Note: requires an `Integration` API key."""
    body = {
        "memories": [
            {
                "external_id": m.external_id,
                "custom_type": m.custom_type,
                "created_at": HttpClient.localize(m.created_at),
                "data": m.data,
            }
            for m in params.memories
        ]
    }
    _ = client.post(path=f"customers/{customer_id}/memories", body=body)
