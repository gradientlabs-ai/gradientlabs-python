import os
import sys
import logging
from datetime import datetime

from gradient_labs import (
    Client,
    CustomerMemory,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = Client(
    api_key=os.environ["GLABS_API_KEY"],
    base_url=os.environ.get("GRADIENT_LABS_BASE_URL", "http://localhost:4000"),
)

# Each memory is scoped to a customer and stores an arbitrary JSON object in
# `data`, kept verbatim for the AI agent to search over on demand. The call is
# asynchronous ("fire and forget") and returns nothing; it raises a 409 Conflict
# if a batch is already being created for the same customer.
client.batch_create_customer_memories(
    customer_id="cust_01ham6bzcdeja9xzqhjf6daq30",
    memories=[
        CustomerMemory(
            external_id="order_456",
            custom_type="order",
            created_at=datetime(2026, 1, 2, 10, 0, 0),
            data={"order_id": "order-456", "total": 42.0},
        ),
        CustomerMemory(
            external_id="pref_email",
            custom_type="preference",
            created_at=datetime(2026, 1, 3, 9, 30, 0),
            data={"channel": "email"},
        ),
    ],
)
logging.info("✅ Customer memories batch accepted")
