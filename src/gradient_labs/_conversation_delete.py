from ._http_client import HttpClient


def delete_conversation(*, client: HttpClient, conversation_id: str) -> None:
    _ = client.delete(
        path=f"conversations/{conversation_id}",
        body=None,
    )
