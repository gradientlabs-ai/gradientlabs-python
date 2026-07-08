from unittest.mock import MagicMock

from gradient_labs import (
    Client,
    Conversation,
    ConversationChannel,
    CustomerSupportPlatformIdentifier,
    CustomerSupportPlatformIdentifierType,
    StartConversationParams,
    SupportPlatform,
)


def _client_returning(response: dict):
    client = Client(api_key="test-key")
    post = MagicMock(return_value=response)
    client.http_client.post = post
    return client, post


def _conversation_response() -> dict:
    return {
        "id": "conv-123",
        "customer_id": "cust-456",
        "channel": "web",
        "status": "active",
        "created": "2024-01-15T10:30:00",
        "updated": "2024-01-15T10:30:00",
    }


def test_start_conversation():
    client, post = _client_returning(_conversation_response())

    conversation = client.start_conversation(
        params=StartConversationParams(
            id="conv-123",
            customer_id="cust-456",
            channel=ConversationChannel.LIVE_CHAT,
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    assert kwargs["path"] == "conversations"
    assert body["id"] == "conv-123"
    assert body["customer_id"] == "cust-456"
    assert body["channel"] == "web"
    assert "customer_support_platform_identifiers" not in body

    assert isinstance(conversation, Conversation)
    assert conversation.id == "conv-123"


def test_start_conversation_includes_customer_support_platform_identifiers():
    client, post = _client_returning(_conversation_response())

    client.start_conversation(
        params=StartConversationParams(
            id="conv-123",
            customer_id="cust-456",
            channel=ConversationChannel.LIVE_CHAT,
            customer_support_platform_identifiers=[
                CustomerSupportPlatformIdentifier(
                    support_platform=SupportPlatform.INTERCOM,
                    type=CustomerSupportPlatformIdentifierType.INTERCOM_USER,
                    value="6953e162a988d9ef0f73ef9b",
                ),
                CustomerSupportPlatformIdentifier(
                    support_platform=SupportPlatform.FRESHDESK,
                    value="fd-789",
                ),
            ],
        )
    )

    _, kwargs = post.call_args
    body = kwargs["body"]
    identifiers = body["customer_support_platform_identifiers"]
    assert identifiers[0]["support_platform"] == "intercom"
    assert identifiers[0]["type"] == "intercom_user"
    assert identifiers[0]["value"] == "6953e162a988d9ef0f73ef9b"
    assert identifiers[1]["support_platform"] == "freshdesk"
    assert identifiers[1]["type"] is None
    assert identifiers[1]["value"] == "fd-789"
