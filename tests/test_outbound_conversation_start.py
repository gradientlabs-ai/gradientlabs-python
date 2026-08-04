from unittest.mock import MagicMock

from gradient_labs import (
    Client,
    CustomerSupportPlatformIdentifier,
    CustomerSupportPlatformIdentifierType,
    OutboundSupportPlatform,
    StartOutboundChatConversationParams,
    StartOutboundConversationResponse,
    StartOutboundEmailConversationParams,
    StartOutboundPhoneConversationParams,
    SupportPlatform,
)


def _client_returning(response: dict):
    client = Client(api_key="test-key")
    post = MagicMock(return_value=response)
    client.http_client.post = post
    return client, post


def test_start_outbound_chat_conversation():
    client, post = _client_returning({"conversation_id": "conv-123"})

    rsp = client.start_outbound_chat_conversation(
        params=StartOutboundChatConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            support_platform=OutboundSupportPlatform.INTERCOM,
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert kwargs["path"] == "outbound/conversations/chat"
    assert body == {
        "customer_id": "cust-456",
        "procedure_id": "procedure-789",
        "support_platform": "intercom",
    }

    assert isinstance(rsp, StartOutboundConversationResponse)
    assert rsp.conversation_id == "conv-123"


def test_start_outbound_chat_conversation_with_optional_fields():
    client, post = _client_returning({"conversation_id": "conv-123"})

    client.start_outbound_chat_conversation(
        params=StartOutboundChatConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            support_platform=OutboundSupportPlatform.PUBLIC_API,
            customer_support_platform_identifiers=[
                CustomerSupportPlatformIdentifier(
                    support_platform=SupportPlatform.INTERCOM,
                    type=CustomerSupportPlatformIdentifierType.INTERCOM_USER,
                    value="6953e162a988d9ef0f73ef9b",
                ),
            ],
            body="Hi there!",
            resources={"customer_profile": {"tier": "premium"}},
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert body["support_platform"] == "public-api"
    assert body["body"] == "Hi there!"
    assert body["resources"] == {"customer_profile": {"tier": "premium"}}
    identifiers = body["customer_support_platform_identifiers"]
    assert identifiers[0]["support_platform"] == "intercom"
    assert identifiers[0]["type"] == "intercom_user"
    assert identifiers[0]["value"] == "6953e162a988d9ef0f73ef9b"


def test_start_outbound_email_conversation():
    client, post = _client_returning({"conversation_id": "conv-123"})

    rsp = client.start_outbound_email_conversation(
        params=StartOutboundEmailConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            support_platform=OutboundSupportPlatform.ZENDESK,
            customer_support_platform_identifiers=[
                CustomerSupportPlatformIdentifier(
                    support_platform=SupportPlatform.ZENDESK,
                    type=CustomerSupportPlatformIdentifierType.ZENDESK_SUPPORT_USER,
                    value="zd-42",
                ),
            ],
            subject="Your order",
            body="It has shipped.",
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert kwargs["path"] == "outbound/conversations/email"
    assert body["customer_id"] == "cust-456"
    assert body["procedure_id"] == "procedure-789"
    assert body["support_platform"] == "zendesk"
    assert body["subject"] == "Your order"
    assert body["body"] == "It has shipped."
    identifiers = body["customer_support_platform_identifiers"]
    assert identifiers[0]["support_platform"] == "zendesk"
    assert identifiers[0]["type"] == "zendesk_support_user"
    assert identifiers[0]["value"] == "zd-42"

    assert rsp.conversation_id == "conv-123"


def test_start_outbound_email_conversation_omits_unset_subject_and_body():
    client, post = _client_returning({"conversation_id": "conv-123"})

    client.start_outbound_email_conversation(
        params=StartOutboundEmailConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            support_platform=OutboundSupportPlatform.SALESFORCE,
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert "subject" not in body
    assert "body" not in body
    assert "customer_support_platform_identifiers" not in body
    assert "resources" not in body


def test_start_outbound_phone_conversation():
    client, post = _client_returning({"conversation_id": "conv-123"})

    rsp = client.start_outbound_phone_conversation(
        params=StartOutboundPhoneConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            to_phone_number="+14155551234",
            from_phone_number="+14155559876",
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert kwargs["path"] == "outbound/conversations/phone"
    assert body == {
        "customer_id": "cust-456",
        "procedure_id": "procedure-789",
        "to_phone_number": "+14155551234",
        "from_phone_number": "+14155559876",
    }
    assert "support_platform" not in body

    assert rsp.conversation_id == "conv-123"


def test_start_outbound_phone_conversation_with_optional_fields():
    client, post = _client_returning({"conversation_id": "conv-123"})

    client.start_outbound_phone_conversation(
        params=StartOutboundPhoneConversationParams(
            customer_id="cust-456",
            procedure_id="procedure-789",
            to_phone_number="+14155551234",
            from_phone_number="+14155559876",
            customer_support_platform_identifiers=[
                CustomerSupportPlatformIdentifier(
                    support_platform=SupportPlatform.SALESFORCE,
                    type=CustomerSupportPlatformIdentifierType.SALESFORCE_CONTACT_ID,
                    value="003xx000004TmiQAAS",
                ),
            ],
            resources={"order": {"id": "ord-1"}},
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert body["resources"] == {"order": {"id": "ord-1"}}
    identifiers = body["customer_support_platform_identifiers"]
    assert identifiers[0]["support_platform"] == "salesforce"
    assert identifiers[0]["type"] == "salesforce_contact_id"
    assert identifiers[0]["value"] == "003xx000004TmiQAAS"
