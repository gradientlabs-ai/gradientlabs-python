import os
from gradient_labs import Client, ParticipantType
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
    message_id="msg123",
    body="Hello, world!",
    participant_type=ParticipantType.CUSTOMER,
    participant_id="user123",
    created=datetime.now(),
)

client.cancel_conversation(conversation_id=conv.id)
