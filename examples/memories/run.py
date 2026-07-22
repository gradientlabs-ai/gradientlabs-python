import os
import sys
import uuid
import logging

from gradient_labs import (
    Client,
    BulkUploadMemoriesParams,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = Client(
    api_key=os.environ["GLABS_API_KEY"],
    base_url="http://localhost:4000",
)

# Each memory is an arbitrary JSON object stored verbatim for the AI agent to
# search over on demand. created_at_keys lists the payload keys tried in order
# to read each memory's timestamp; when none match, the upload time is used.
rsp = client.bulk_upload_conversation_memories(
    conversation_id="conv_01ham6bzcdeja9xzqhjf6daq30",
    params=BulkUploadMemoriesParams(
        idempotency_key=str(uuid.uuid4()),
        memories=[
            {
                "kind": "preference",
                "channel": "email",
                "occurred_at": "2026-01-02T10:00:00Z",
            },
            {"kind": "order", "order_id": "order-456", "total": 42.0},
        ],
        created_at_keys=["occurred_at"],
    ),
)
logging.info(
    f"✅ Memories uploaded: {rsp.memories_inserted} inserted (upload {rsp.upload_id})"
)
