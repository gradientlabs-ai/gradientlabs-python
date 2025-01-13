from datetime import datetime
from typing import Any, List, Optional

from .webhook import Webhook, WebhookEvent
from .types import ParticipantType, Conversation, Attachment

from ._http_client import HttpClient, API_BASE_URL


class Client:
    """Client is the client for the Gradient Labs
    public api. For full details, please refer to the online docs:

    https://api-docs.gradient-labs.ai/
    """

    def __init__(
        self,
        *,
        api_key: str,
        signing_key: Optional[str] = None,
        base_url: Optional[str] = API_BASE_URL,
        timeout: Optional[int] = None,
    ):
        self.http_client = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.signing_key = signing_key

    def assign_conversation(
        self,
        *,
        conversation_id: str,
        participant_type: ParticipantType,
        assignee_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Assigns a conversation to the given participant."""
        body = {"assignee_type": participant_type}
        if assignee_id:
            body["assignee_id"] = assignee_id
        if timestamp:
            body["timestamp"] = HttpClient.localize(timestamp)
        _ = self.http_client.put(
            f"conversations/{conversation_id}/assignee",
            body,
        )

    def finish_conversation(
        self, *, conversation_id: str, timestamp: Optional[datetime] = None
    ) -> None:
        """Finishes the conversation"""
        body = {}
        if timestamp is not None:
            body["timestamp"] = HttpClient.localize(timestamp)
        _ = self.http_client.put(
            f"conversations/{conversation_id}/finish",
            body,
        )

    def read_conversation(self, *, conversation_id: str) -> Conversation:
        """Retrieves the conversation"""
        body = self.http_client.get(
            f"conversations/{conversation_id}",
            {},
        )
        return Conversation.from_dict(body)

    def start_conversation(
        self,
        *,
        conversation_id: str,
        customer_id: str,
        channel: str,
        created: Optional[datetime] = None,
        metadata: Optional[Any] = None,
    ) -> Conversation:
        """Starts a conversation."""
        body = {
            "id": conversation_id,
            "customer_id": customer_id,
            "channel": channel,
        }
        if metadata is not None:
            body["metadata"] = metadata
        if created is not None:
            body["created"] = HttpClient.localize(created)
        rsp = self.http_client.post(
            "conversations",
            body,
        )
        return Conversation.from_dict(rsp)

    def add_message(
        self,
        *,
        message_id: str,
        conversation_id: str,
        body: str,
        participant_id: str,
        participant_type: ParticipantType,
        created: Optional[datetime] = None,
        attachments: List[Attachment] = None,
    ) -> None:
        """Adds a message to a conversation."""
        body = {
            "id": message_id,
            "body": body,
            "participant_id": participant_id,
            "participant_type": participant_type,
        }
        if created is not None:
            body["created"] = HttpClient.localize(created)
        if attachments is not None and len(attachments) != 0:
            body["attachments"] = [a.to_dict() for a in attachments]

        _ = self.http_client.post(
            f"conversations/{conversation_id}/messages",
            body,
        )

    def add_resource(
        self,
        *,
        conversation_id: str,
        name: str,
        data: Any,
    ) -> None:
        """Attaches a resource to the conversation."""
        _ = self.http_client.put(
            f"conversations/{conversation_id}/resources/{name}",
            data,
        )

    def upsert_hand_off_target(self, *, hand_off_target_id: str, name: str) -> None:
        """Inserts or updates a hand-off target."""
        _ = self.http_client.post(
            f"hand-off-targets",
            {
                "id": hand_off_target_id,
                "name": name,
            },
        )

    def parse_webhook(self, payload: str, signature_header: str) -> WebhookEvent:
        return Webhook.parse_event(
            payload=payload,
            signature_header=signature_header,
            signing_key=self.signing_key,
        )
