from typing import Optional, Dict, Any
from enum import Enum

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


class CustomerSource(str, Enum):
    """Identifies where customer data originates from."""

    INTERCOM = "intercom"
    FRESHCHAT = "freshchat"
    FRESHDESK = "freshdesk"
    PUBLIC_API = "public-api"
    SALESFORCE = "salesforce"
    ZENDESK = "zendesk"
    VOICE = "livekit"
    VOICE_TWILIO = "twilio"
    VOICE_TALKDESK = "talkdesk"
    VOICE_INTERCOM = "intercom-voice"
    WEB_APP = "web-app"
    FILE = "file"


class SupportPlatform(str, Enum):
    """Identifies the support platform where the conversation will be created."""

    FRESHCHAT = "freshchat"
    FRESHDESK = "freshdesk"
    INTERCOM = "intercom"
    PUBLIC_API = "public-api"
    SALESFORCE = "salesforce"
    ZENDESK = "zendesk"
    VOICE = "livekit"
    VOICE_TWILIO = "twilio"
    VOICE_TALKDESK = "talkdesk"
    VOICE_INTERCOM = "intercom-voice"
    WEB_APP = "web-app"


@dataclass_json
@dataclass(frozen=True)
class StartOutboundConversationParams:
    """Parameters for starting a new outbound conversation.

    This kicks off a proactive conversation where your AI agent initiates
    contact with a customer.
    """

    # customer_id is the external identifier for the customer in your support platform.
    # For Intercom, this is the external ID you've defined for the user (e.g., "user-123456").
    # For other platforms, this is the customer identifier used by that platform.
    customer_id: str

    # customer_source is the source of the customer data.
    # For example, a customer ID and phone number might be from Intercom, but the outbound
    # conversation is initiated via Twilio.
    customer_source: CustomerSource

    # procedure_id is the ID of the outbound procedure that defines what the AI agent
    # should accomplish in this conversation. The procedure must be of type "outbound"
    # and must be live (deployed).
    procedure_id: str

    # support_platform is the support platform where the conversation should be created.
    # Valid values include "intercom", "zendesk", "freshdesk", "freshchat".
    # If not provided, the system will automatically select the first connected platform
    # in priority order: intercom, zendesk, freshchat, freshdesk, public-api.
    support_platform: Optional[SupportPlatform] = None

    # channel specifies the communication channel for this conversation.
    # If not provided, defaults to "email".
    # Valid values: "email", "web", "sms", "voice", etc.
    channel: Optional[str] = None

    # subject is the subject line for the initial message (primarily used for email channels).
    # Only used if body is also provided. If both subject and body are omitted, the AI agent
    # will generate the initial message.
    subject: Optional[str] = None

    # body is the content of the initial message to send to the customer.
    # If provided, this message will be sent instead of having the AI agent generate one.
    # If omitted, the AI agent will generate an appropriate initial message based on the procedure.
    body: Optional[str] = None

    # resources is a JSON object containing structured data that the AI agent
    # can use during the conversation. This should be organized as a dict
    # where keys are resource type names and values are the corresponding data.
    # Example: {"customer_profile": {"tier": "premium", "lifetime_value": 5000}}
    # The data will be made available to the AI agent for context during conversation processing.
    resources: Optional[Dict[str, Any]] = None


@dataclass_json
@dataclass(frozen=True)
class StartOutboundConversationResponse:
    """Response from starting an outbound conversation."""

    # conversation_id is the internal identifier for the created conversation.
    # You can use this ID with other conversation APIs to check status, send messages, etc.
    conversation_id: str


def start_outbound_conversation(
    *, client: HttpClient, params: StartOutboundConversationParams
) -> StartOutboundConversationResponse:
    """Creates and starts a new outbound conversation where the AI agent
    proactively initiates contact with a customer.

    The conversation follows the instructions defined in the specified outbound procedure.

    If support_platform is not provided, the system will automatically select the highest
    priority platform that has integration settings configured for your company.

    If body and subject are provided, that message will be sent as the initial message.
    Otherwise, the AI agent will generate an appropriate initial message based on the procedure.
    """
    body = {
        "customer_id": params.customer_id,
        "customer_source": params.customer_source.value
        if isinstance(params.customer_source, CustomerSource)
        else params.customer_source,
        "procedure_id": params.procedure_id,
    }

    if params.support_platform is not None:
        body["support_platform"] = (
            params.support_platform.value
            if isinstance(params.support_platform, SupportPlatform)
            else params.support_platform
        )
    if params.channel is not None:
        body["channel"] = params.channel
    if params.subject is not None:
        body["subject"] = params.subject
    if params.body is not None:
        body["body"] = params.body
    if params.resources is not None:
        body["resources"] = params.resources

    rsp = client.post(
        path="outbound/conversations",
        body=body,
    )
    return StartOutboundConversationResponse.from_dict(rsp)
