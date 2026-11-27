from ._http_client import HttpClient
from .conversation import Conversation


def read_conversation_deprecated(
    *, client: HttpClient, conversation_id: str
) -> Conversation:
    """read_conversation_deprecated retrieves the conversation from the deprecated
    `GET /conversations/{id}` endpoint. Use read_conversation instead."""
    rsp = client.get(path=f"conversations/{conversation_id}")
    return Conversation.from_dict(rsp)
