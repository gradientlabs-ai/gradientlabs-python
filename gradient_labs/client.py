from typing import Any, Optional

from .conversation import Conversation
from ._conversation_assign import assign_conversation, AssignmentParams
from ._conversation_finish import finish_conversation, FinishParams
from ._conversation_read import read_conversation
from ._conversation_start import start_conversation, StartConversationParams
from ._http_client import HttpClient, API_BASE_URL
from ._message import add_message, AddMessageParams, Message
from ._http_client import HttpClient, API_BASE_URL
from .webhook import Webhook, WebhookEvent


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
        params: AssignmentParams,
    ) -> None:
        """Assigns a conversation to the given participant."""
        assign_conversation(
            client=self.client,
            conversation_id=conversation_id,
            params=params,
        )

    def finish_conversation(
        self,
        *,
        conversation_id: str,
        params: FinishParams,
    ) -> None:
        """finish_conversation finishes a conversation.

        A conversation finishes when it has come to its natural conclusion. This could be because
        the customer's query has been resolved, a human agent or other automation has closed the chat,
        or because the chat is being closed due to inactivity."""
        finish_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def read_conversation(self, *, conversation_id: str) -> Conversation:
        """Retrieves the conversation"""
        return read_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
        )

    def start_conversation(
        self,
        *,
        params: StartConversationParams,
    ) -> Conversation:
        """Starts a conversation."""
        return start_conversation(
            client=self.http_client,
            params=params,
        )

    def add_message(
        self,
        *,
        conversation_id: str,
        params: AddMessageParams,
    ) -> Message:
        """Adds a message to a conversation."""
        return add_message(
            client=self.client,
            conversation_id=conversation_id,
            params=params,
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
