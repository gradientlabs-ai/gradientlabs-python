from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


class ParticipantType(str, Enum):

    """ A participant type identifies the type of user who has
    sent a message in a conversation. """

    CUSTOMER: str = "Customer"
    AGENT: str = "Agent"


@dataclass_json
@dataclass(frozen=True)
class Conversation:

    """ A conversation is the primary way that a customer
    talks to our AI agent.
    """

    id: str
    customer_id: str
    metadata: dict
    status: str
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
