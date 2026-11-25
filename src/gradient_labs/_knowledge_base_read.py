from ._http_client import HttpClient
from .knowledge_base import KnowledgeBase


def read_knowledge_base(*, client: HttpClient, knowledge_base_id: str) -> KnowledgeBase:
    """read_knowledge_base retrieves a knowledge base by your own ID for it.

    Note: requires an `Integration` or `Management` API key."""
    rsp = client.get(path=f"knowledge-bases/{knowledge_base_id}")
    return KnowledgeBase.from_dict(rsp)
