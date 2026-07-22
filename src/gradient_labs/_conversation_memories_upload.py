from typing import Optional, List, Dict, Any

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class BulkUploadMemoriesParams:
    # idempotency_key de-duplicates retries of the same upload. Re-uploading with
    # the same key returns the original upload instead of inserting again.
    idempotency_key: str

    # memories is the list of individual memories to store. Each element is an
    # arbitrary JSON object stored verbatim as the memory's raw payload.
    memories: List[Dict[str, Any]]

    # created_at_keys optionally lists JSON keys tried in order to read each
    # memory's timestamp from its payload. When none match, the upload time is used.
    created_at_keys: Optional[List[str]] = None


@dataclass_json
@dataclass(frozen=True)
class BulkUploadMemoriesResponse:
    # upload_id identifies the upload that stored these memories.
    upload_id: str

    # memories_inserted is the number of memories that were stored.
    memories_inserted: int


def bulk_upload_conversation_memories(
    *, client: HttpClient, conversation_id: str, params: BulkUploadMemoriesParams
) -> BulkUploadMemoriesResponse:
    """bulk_upload_conversation_memories stores a batch of memories scoped to a
    conversation, for the AI agent to search over on demand."""
    body: Dict[str, Any] = {
        "idempotency_key": params.idempotency_key,
        "memories": params.memories,
    }
    if params.created_at_keys is not None:
        body["created_at_keys"] = params.created_at_keys

    rsp = client.post(
        path=f"conversations/{conversation_id}/memories",
        body=body,
    )
    return BulkUploadMemoriesResponse.from_dict(rsp)
