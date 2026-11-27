from typing import Optional
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
from typing import Any, Dict

from ._datetime import parse_datetime

from .back_office_task import BackOfficeTask


class ParticipantType(str, Enum):
    """A participant type identifies the type of user who has
    sent a message in a conversation."""

    CUSTOMER: str = "Customer"
    HUMAN_AGENT: str = "Agent"
    AI_AGENT: str = "AI Agent"
    BOT: str = "Bot"


class ConversationChannel(str, Enum):
    """A channel identifies how the customer has gotten
    in touch with customer support."""

    EMAIL: str = "email"
    LIVE_CHAT: str = "web"
    VOICE: str = "voice"


class AttachmentType(str, Enum):
    """An attachment type identifies the type of file
    that a customer has uploaded into the conversation."""

    IMAGE: str = "image"
    FILE: str = "file"


class ConversationEventType(str, Enum):
    """ConversationEventType describes an event that occurred within the conversation."""

    # INTERNAL_NOTE means that an internal note has been added to the conversation.
    INTERNAL_NOTE: str = "internal-note"

    # DELIVERED means that a message has been delivered
    # to a participant
    DELIVERED: str = "delivered"

    # MESSAGE_READ means that a message has been read
    # by the participant it was delivered to
    MESSAGE_READ: str = "read"

    # TYPING means the customer or human agent started typing.
    TYPING: str = "typing"


@dataclass_json
@dataclass(frozen=True)
class AgentMetadata:
    intent: Optional[str] = None
    intent_hand_off_target: Optional[str] = field(
        default=None, metadata=config(field_name="intent_handoff_target")
    )
    hand_off_reason: Optional[str] = field(
        default=None, metadata=config(field_name="handoff_reason")
    )
    hand_off_note: Optional[str] = field(
        default=None, metadata=config(field_name="handoff_note")
    )


@dataclass_json
@dataclass(frozen=True)
class Conversation:
    """A conversation is the primary way that a customer
    talks to our AI agent.
    """

    id: str
    customer_id: str
    channel: ConversationChannel

    status: str
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    is_active: bool = field(
        default=False, metadata=config(field_name="agent_is_active")
    )
    latest_intent: Optional[str] = None
    latest_hand_off_target: Optional[str] = field(
        default=None, metadata=config(field_name="latest_handoff_target")
    )
    agent_metadata: Optional[AgentMetadata] = field(
        default=None, metadata=config(field_name="latest_agent_metadata")
    )


@dataclass_json
@dataclass(frozen=True)
class Attachment:
    # type of file that was uploaded.
    type: AttachmentType

    # file_name is the name of the file that was uploaded, or an
    # adequate placeholder for that name, which can be shown to reviewers.
    file_name: str

    # url is the publicly accessible URL where the attachment can be downloaded
    # from. This should be a fully qualified URL. If not given, the AI agent will
    # only know that an attachment exists, but will be unable to process it.
    url: Optional[str] = None

    # summary is an optional short summary of the attachment.  This is only intended
    # to be used if you cannot give us access to the raw attachment, but can
    # run your own LLM completions on the attachment and send us a description instead.
    #
    # If a summary or description is provided, then there must be no URL.
    summary: Optional[str] = None

    # description is an optional description of the attachment. This is only intended
    # to be used if you cannot give us access to the raw attachment, but can
    # run your own LLM completions on the attachment and send us a description instead.
    #
    # Chat to us first before using it!
    description: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class WebhookConversation:
    """
    Details of the conversation the event relates to.
    """

    conversation_id: str = field(metadata=config(field_name="id"))
    """
    The conversation's assigned identifier.
    """

    customer_id: str
    """
    The customer's assigned identifier.
    """

    customer_source: Optional[str] = None
    """
    The support platform the customer comes from, such as `intercom`. Only
    present on action.execute events.
    """

    metadata: Optional[Any] = None
    """
    Extra details about the conversation. Only present on action.execute events.
    """


@dataclass_json
@dataclass(frozen=True)
class AgentMessageEvent:
    """
    An event that represents a message from the agent.
    """

    conversation: WebhookConversation
    """
    Details of the conversation the event relates to.
    """

    body: str
    """
    Text of the agent's message.
    """

    total: Optional[int] = 0
    """
    total identifies the number of agent messages that have been
	produced in the current turn.
    """

    sequence: Optional[int] = 0
    """
    sequence identifies which agent message this is in the current turn.
    """

    intent: Optional[str] = None
    """
    intent is the most recent intent that was classified from the customer's
    conversation, if any.
    """

    is_holding: Optional[bool] = False
    """
    is_holding identifies whether the agent message is a holding-response or not.
    Holding-responses are sent to let the customer know that the agent is working on a full response.
    For example: "I'm sorry to hear you want to close your account. Let me take a look at the next steps for you..."
    """


@dataclass_json
@dataclass(frozen=True)
class ConversationHandOffEvent:
    conversation: WebhookConversation
    """
    Details of the conversation the event relates to.
    """
    reason_code: str
    """
    reason_code is the code that describes why the agent wants to hand off this
    conversation.
    """

    reason: str
    """
    reason is a human-legible description of the Reason code.
    """

    note: Optional[str] = None
    """
    Note is a human-legible summary of the conversation so far, for a smooth hand-off.
    """

    intent: Optional[str] = None
    """
    Intent is the most recent intent that was classified from the customer's conversation, if any.
    """

    target: Optional[str] = None
    """
    Target defines where the agent wants to hand this conversation to.
    """


@dataclass_json
@dataclass(frozen=True)
class ConversationFinishedEvent:
    conversation: WebhookConversation
    """
    Details of the conversation the event relates to.
    """

    intent: Optional[str] = None
    """
    Intent is the most recent intent that was classified from the customer's conversation, if any.
    """

    reason_code: Optional[str] = None
    """
    reason_code is the code that describes why the conversation finished, if known.
    """


@dataclass_json
@dataclass(frozen=True)
class WebhookBackOfficeTask:
    """
    Details of the back-office task the event relates to.
    """

    id: str
    """
    The back-office task's identifier.
    """


@dataclass_json
@dataclass(frozen=True)
class ActionExecuteEvent:
    action: str
    """
    The action's given identifier.
    """

    params: Dict[str, Any]
    """
    Parameters the agent has generated for this action.
    """

    conversation: Optional[WebhookConversation] = None
    """
    Details of the conversation the event relates to. Not set when the action
    runs for a back-office task.
    """

    back_office_task: Optional[WebhookBackOfficeTask] = None
    """
    Details of the back-office task the event relates to. Only set when the
    action runs for a back-office task.
    """


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskCompleteEvent:
    """
    An event that says a back-office task has completed.
    """

    back_office_task: BackOfficeTask
    """
    The back-office task.
    """


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskHandOffEvent:
    """
    An event that says a back-office task has been handed off to a human.
    """

    back_office_task: BackOfficeTask
    """
    The back-office task.
    """


@dataclass_json
@dataclass(frozen=True)
class BackOfficeTaskFailEvent:
    """
    An event that says a back-office task has failed.
    """

    back_office_task: BackOfficeTask
    """
    The back-office task.
    """


@dataclass_json
@dataclass(frozen=True)
class ConversationStartEvent:
    """
    An event asking you to open an outbound conversation with a customer.
    Answer it with a ConversationStartResponse.
    """

    customer_id: str
    """
    Your identifier for the customer to contact.
    """

    channel: ConversationChannel
    """
    How to contact the customer.
    """

    body: str
    """
    The first message to send to the customer.
    """

    subject: str
    """
    The subject line, for email conversations. Empty on other channels.
    """

    initiator_id: str
    """
    Who started the outbound conversation: `public-api` when you started it
    through the API. Otherwise the Gradient Labs ID of the conversation or
    back-office task that started it.
    """


@dataclass_json
@dataclass(frozen=True)
class ConversationStartResponse:
    """
    The body to answer a conversation.start event with.
    """

    conversation_id: str
    """
    Your identifier for the conversation you opened. Use it in later API calls
    about this conversation.
    """


@dataclass_json
@dataclass(frozen=True)
class WebhookEvent:
    event_id: str = field(metadata=config(field_name="id"))
    """
    Unique identifier for this event.
    """

    event_type: str = field(metadata=config(field_name="type"))
    """
    Type of event (see: https://api-docs.gradient-labs.ai/#webhooks).
    """

    sequence_number: int
    """
    Sequential index of this event within the conversation (see: https://api-docs.gradient-labs.ai/#sequence-numbers).
    """

    timestamp: datetime = field(
        metadata=config(decoder=parse_datetime, mm_field=fields.DateTime(format="iso"))
    )
    """
    Time at which this event was generated.
    """

    data: Any
    """
    Event data
    """
