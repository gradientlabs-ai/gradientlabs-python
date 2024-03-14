import os
import uuid
from gradient_labs import Client, ParticipantType, Attachment, AttachmentType
from datetime import datetime

client = Client(
    api_key=os.environ["GLABS_API_KEY"],
    base_url="http://localhost:4000",
)

conv = client.start_conversation(
    conversation_id="python-conversation-12345",
    customer_id="snake",
)

client.add_message(
    conversation_id=conv.id,
    id=uuid.uuid4(),
    body="Hello, how can we help you?",
    participant_type=ParticipantType.CUSTOMER,
    participant_id="bot",
)

client.add_message(
    conversation_id=conv.id,
    id=uuid.uuid4(),
    body="Hello, world! Could I have a bank statement?",
    participant_type=ParticipantType.CUSTOMER,
    participant_id="user_123",
    created=datetime.now(),
)

client.add_message(
    conversation_id=conv.id,
    id=uuid.uuid4(),
    body="Sure, here it is!",
    participant_type=ParticipantType.HUMAN_AGENT,
    participant_id="agent_123",
    attachments=[
        Attachment(
            type=AttachmentType.FILE,
            file_name="bank_statement.pdf",
        )
    ],
)

client.cancel_conversation(id=conv.id)
