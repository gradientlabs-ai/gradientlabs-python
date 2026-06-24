import os
import sys
import uuid
import logging

from gradient_labs import (
    Client,
    BackOfficeTaskCreateParams,
    BackOfficeTaskCreateAttachment,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

client = Client(
    api_key=os.environ["GLABS_API_KEY"],
    base_url="http://localhost:4000",
)

# agent_id is the agent (agent group, prefix `agent_`) that runs the task, and
# procedure_id is the procedure (prefix `proc_`) within that agent to start from.
task = client.create_back_office_task(
    params=BackOfficeTaskCreateParams(
        id=str(uuid.uuid4()),
        agent_id="agent_01ham6bzcdeja9xzqhjf6daq30",
        procedure_id="proc_01ham6bzcdeja9xzqhjf6daq30",
        input={"order_id": "order-456"},
        metadata={"team": "billing"},
        attachments=[
            BackOfficeTaskCreateAttachment(
                file_name="document.pdf",
                url="https://example.com/document.pdf",
            )
        ],
    )
)
logging.info(f"✅ Back-office task created: {task.id} (status: {task.status})")
