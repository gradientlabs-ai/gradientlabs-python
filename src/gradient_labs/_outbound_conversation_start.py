from typing import Optional, Dict, Any, List
from enum import Enum

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from ._conversation_start import CustomerSupportPlatformIdentifier


class OutboundSupportPlatform(str, Enum):
    """Identifies the support platform an outbound chat or email is delivered on."""

    INTERCOM: str = "intercom"
    ZENDESK: str = "zendesk"
    SALESFORCE: str = "salesforce"

    # PUBLIC_API delivers the conversation to your own webhook endpoint.
    PUBLIC_API: str = "public-api"


@dataclass_json
@dataclass(frozen=True)
class StartOutboundChatConversationParams:
    """Parameters for starting an outbound live chat conversation."""

    # customer_id is your own identifier for the customer, as used in your systems.
    # It is stored as the customer's company customer ID, and is the identifier echoed
    # back to you in tool and webhook payloads.
    customer_id: str

    # procedure_id is the ID of the outbound procedure that defines what the AI agent
    # should accomplish in this conversation. The procedure must be of type "outbound",
    # must be live (deployed), and must be enabled for the chat channel.
    procedure_id: str

    # support_platform is the support platform the chat is delivered on.
    # Valid values: "intercom", "public-api".
    support_platform: OutboundSupportPlatform

    # customer_support_platform_identifiers optionally links the customer to their
    # record(s) in third-party support platforms (e.g. Intercom), alongside customer_id.
    #
    # The platform named in support_platform needs an identifier here, unless the
    # customer already carries one from an earlier conversation.
    customer_support_platform_identifiers: Optional[
        List[CustomerSupportPlatformIdentifier]
    ] = None

    # body is the content of the initial message to send to the customer.
    # If omitted, the AI agent will generate an appropriate opening message based on
    # the procedure.
    body: Optional[str] = None

    # resources is a JSON object containing structured data that the AI agent
    # can use during the conversation. This should be organized as a dict
    # where keys are resource type names and values are the corresponding data.
    # Example: {"customer_profile": {"tier": "premium", "lifetime_value": 5000}}
    resources: Optional[Dict[str, Any]] = None


@dataclass_json
@dataclass(frozen=True)
class StartOutboundEmailConversationParams:
    """Parameters for starting an outbound email conversation."""

    # customer_id is your own identifier for the customer, as used in your systems.
    # It is stored as the customer's company customer ID, and is the identifier echoed
    # back to you in tool and webhook payloads.
    customer_id: str

    # procedure_id is the ID of the outbound procedure that defines what the AI agent
    # should accomplish in this conversation. The procedure must be of type "outbound",
    # must be live (deployed), and must be enabled for the email channel.
    procedure_id: str

    # support_platform is the support platform the email is sent from.
    # Valid values: "intercom", "zendesk", "salesforce", "public-api".
    support_platform: OutboundSupportPlatform

    # customer_support_platform_identifiers optionally links the customer to their
    # record(s) in third-party support platforms (e.g. Intercom, Zendesk, Salesforce),
    # alongside customer_id.
    #
    # The platform named in support_platform needs an identifier here, unless the
    # customer already carries one from an earlier conversation. Zendesk requires type
    # "zendesk_support_user"; Salesforce requires type "salesforce_contact_id".
    customer_support_platform_identifiers: Optional[
        List[CustomerSupportPlatformIdentifier]
    ] = None

    # subject is the subject line for the initial email. Required if body is provided,
    # and forbidden otherwise. If both are omitted, the AI agent will write the opening
    # email.
    subject: Optional[str] = None

    # body is the content of the initial email to send to the customer. Required if
    # subject is provided, and forbidden otherwise.
    body: Optional[str] = None

    # resources is a JSON object containing structured data that the AI agent
    # can use during the conversation. This should be organized as a dict
    # where keys are resource type names and values are the corresponding data.
    # Example: {"customer_profile": {"tier": "premium", "lifetime_value": 5000}}
    resources: Optional[Dict[str, Any]] = None


@dataclass_json
@dataclass(frozen=True)
class StartOutboundPhoneConversationParams:
    """Parameters for placing an outbound phone call."""

    # customer_id is your own identifier for the customer, as used in your systems.
    # It is stored as the customer's company customer ID, and is the identifier echoed
    # back to you in tool and webhook payloads.
    customer_id: str

    # procedure_id is the ID of the outbound procedure that defines what the AI agent
    # should accomplish on the call. The procedure must be of type "outbound", must be
    # live (deployed), and must be enabled for the "voice" channel.
    procedure_id: str

    # to_phone_number is the customer's phone number to dial (E.164 format,
    # e.g. "+14155551234").
    to_phone_number: str

    # from_phone_number is the caller ID to place the call from (E.164 format).
    # It must be a phone number already provisioned for your company.
    from_phone_number: str

    # customer_support_platform_identifiers optionally links the customer to their
    # record(s) in third-party support platforms (e.g. Intercom, Zendesk, Salesforce),
    # alongside customer_id. They are also used to pull that platform's customer data
    # into the call as context.
    customer_support_platform_identifiers: Optional[
        List[CustomerSupportPlatformIdentifier]
    ] = None

    # resources is a JSON object containing structured data that the AI agent
    # can use during the conversation. This should be organized as a dict
    # where keys are resource type names and values are the corresponding data.
    # Example: {"customer_profile": {"tier": "premium", "lifetime_value": 5000}}
    resources: Optional[Dict[str, Any]] = None


@dataclass_json
@dataclass(frozen=True)
class StartOutboundConversationResponse:
    """Response from starting an outbound conversation."""

    # conversation_id is the internal identifier for the created conversation.
    # You can use this ID with other conversation APIs to check status, send messages, etc.
    conversation_id: str


def _support_platform_value(platform: OutboundSupportPlatform) -> str:
    return platform.value if isinstance(platform, OutboundSupportPlatform) else platform


def _identifiers(
    identifiers: List[CustomerSupportPlatformIdentifier],
) -> List[Dict[str, Any]]:
    return [i.to_dict() for i in identifiers]


def start_outbound_chat_conversation(
    *, client: HttpClient, params: StartOutboundChatConversationParams
) -> StartOutboundConversationResponse:
    """Creates and starts a new outbound live chat conversation in which the AI agent
    proactively initiates contact with a customer, following the instructions defined
    in the specified outbound procedure.

    If body is provided, that message will be sent as the opening message. Otherwise,
    the AI agent will generate one based on the procedure.

    The customer is created, or matched to an existing record, from customer_id and any
    customer_support_platform_identifiers you supply. The platform the chat is delivered
    on needs an identifier for that customer.
    """
    body = {
        "customer_id": params.customer_id,
        "procedure_id": params.procedure_id,
        "support_platform": _support_platform_value(params.support_platform),
    }

    if params.customer_support_platform_identifiers is not None:
        body["customer_support_platform_identifiers"] = _identifiers(
            params.customer_support_platform_identifiers
        )
    if params.body is not None:
        body["body"] = params.body
    if params.resources is not None:
        body["resources"] = params.resources

    rsp = client.post(
        path="outbound/conversations/chat",
        body=body,
    )
    return StartOutboundConversationResponse.from_dict(rsp)


def start_outbound_email_conversation(
    *, client: HttpClient, params: StartOutboundEmailConversationParams
) -> StartOutboundConversationResponse:
    """Creates and starts a new outbound email conversation in which the AI agent
    proactively initiates contact with a customer, following the instructions defined
    in the specified outbound procedure.

    If body and subject are provided, that email will be sent as the opening message.
    Otherwise, the AI agent will write one based on the procedure.

    The customer is created, or matched to an existing record, from customer_id and any
    customer_support_platform_identifiers you supply. The platform the email is sent
    from needs an identifier for that customer, so sending from Zendesk needs a Zendesk
    identifier, and so on.
    """
    body = {
        "customer_id": params.customer_id,
        "procedure_id": params.procedure_id,
        "support_platform": _support_platform_value(params.support_platform),
    }

    if params.customer_support_platform_identifiers is not None:
        body["customer_support_platform_identifiers"] = _identifiers(
            params.customer_support_platform_identifiers
        )
    if params.subject is not None:
        body["subject"] = params.subject
    if params.body is not None:
        body["body"] = params.body
    if params.resources is not None:
        body["resources"] = params.resources

    rsp = client.post(
        path="outbound/conversations/email",
        body=body,
    )
    return StartOutboundConversationResponse.from_dict(rsp)


def start_outbound_phone_conversation(
    *, client: HttpClient, params: StartOutboundPhoneConversationParams
) -> StartOutboundConversationResponse:
    """Places an outbound phone call in which the AI agent proactively contacts a
    customer, following the instructions defined in the specified outbound procedure.

    from_phone_number must be a phone number already provisioned for your company.

    The customer is created, or matched to an existing record, from customer_id and any
    customer_support_platform_identifiers you supply. The dialled number is recorded
    against that same customer.
    """
    body = {
        "customer_id": params.customer_id,
        "procedure_id": params.procedure_id,
        "to_phone_number": params.to_phone_number,
        "from_phone_number": params.from_phone_number,
    }

    if params.customer_support_platform_identifiers is not None:
        body["customer_support_platform_identifiers"] = _identifiers(
            params.customer_support_platform_identifiers
        )
    if params.resources is not None:
        body["resources"] = params.resources

    rsp = client.post(
        path="outbound/conversations/phone",
        body=body,
    )
    return StartOutboundConversationResponse.from_dict(rsp)
