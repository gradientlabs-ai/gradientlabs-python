from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .conversation import ParticipantType, ConversationChannel, Conversation


class SupportPlatform(str, Enum):
    """Identifies a third-party customer support platform that a customer
    can be linked to via a CustomerSupportPlatformIdentifier."""

    INTERCOM: str = "intercom"
    ZENDESK: str = "zendesk"
    SALESFORCE: str = "salesforce"
    FRESHCHAT: str = "freshchat"
    FRESHDESK: str = "freshdesk"


class CustomerSupportPlatformIdentifierType(str, Enum):
    """Identifies the kind of identifier within a customer support platform,
    for platforms that have more than one kind of identifier."""

    INTERCOM_LEAD: str = "intercom_lead"
    INTERCOM_USER: str = "intercom_user"
    ZENDESK_CONVERSATION_USER: str = "zendesk_conversation_user"
    ZENDESK_SUPPORT_USER: str = "zendesk_support_user"
    SALESFORCE_CONTACT_ID: str = "salesforce_contact_id"
    SALESFORCE_ACCOUNT_ID: str = "salesforce_account_id"


@dataclass_json
@dataclass(frozen=True)
class CustomerSupportPlatformIdentifier:
    # support_platform identifies the third-party customer support platform
    # this identifier belongs to.
    support_platform: SupportPlatform

    # value is the customer's external identifier in that platform.
    value: str

    # type optionally identifies which kind of identifier this is, for platforms
    # that have more than one kind (e.g. Intercom leads vs. users). Omit for
    # platforms that only have a single identifier kind (freshchat, freshdesk).
    type: Optional[CustomerSupportPlatformIdentifierType] = None


@dataclass_json
@dataclass(frozen=True)
class StartConversationParams:
    # id uniquely identifies the conversation.
    #
    # Can be anything consisting of letters, numbers, or any of the following
    # characters: _ - + =.
    #
    # Tip: use something meaningful to your business (e.g. a ticket number).
    id: str

    # customer_id uniquely identifies the customer. Used to build historical
    # context of conversations the agent has had with this customer.
    customer_id: str

    # channel represents the way a customer is getting in touch. It will be used
    # to determine how the agent formats responses, etc.
    channel: ConversationChannel

    # assignee_id optionally identifies who the conversation is assigned to.
    assignee_id: Optional[str] = None

    # assignee_type optionally identifies which type of participant is currently
    # assigned to respond. Set this to ParticipantTypeAIAgent to assign the conversation
    # to the Gradient Labs AI when starting it.
    assignee_type: Optional[ParticipantType] = None

    # created optionally defines the time when the conversation started.
    # If not given, this will default to the current time.
    created: Optional[datetime] = None

    # resources is an arbitrary object attached to the conversation and available to the AI agent
    # during the conversation. You can also use resources as parameters for your tools.
    resources: Optional[Dict[str, Any]] = None

    # conversation_token is the raw sensitive token that can be optionally provided when starting a conversation.
    # The latest token of the conversation will be echoed back in future Webhooks, under the header `X-GradientLabs-Token`,
    # as well as in HTTP Tools using templates.
    conversation_token: Optional[str] = None

    # traffic_group_id optionally restricts the conversation to only access procedures
    # assigned to the specified traffic group, plus any procedures not assigned to any group.
    traffic_group_id: Optional[str] = None

    # customer_support_platform_identifiers optionally links the customer to their
    # record(s) in third-party customer support platforms (e.g. Intercom, Zendesk),
    # alongside customer_id.
    customer_support_platform_identifiers: Optional[
        List[CustomerSupportPlatformIdentifier]
    ] = None


def start_conversation(
    *, client: HttpClient, params: StartConversationParams
) -> Conversation:
    body = {
        "id": params.id,
        "customer_id": params.customer_id,
        "channel": params.channel.value,
    }
    if params.created is not None:
        body["created"] = HttpClient.localize(params.created)
    if params.resources is not None:
        body["resources"] = params.resources
    if params.conversation_token is not None:
        body["conversation_token"] = params.conversation_token
    if params.traffic_group_id is not None:
        body["traffic_group_id"] = params.traffic_group_id
    if params.customer_support_platform_identifiers is not None:
        body["customer_support_platform_identifiers"] = [
            i.to_dict() for i in params.customer_support_platform_identifiers
        ]

    rsp = client.post(
        path="conversations",
        body=body,
    )
    return Conversation.from_dict(rsp)
