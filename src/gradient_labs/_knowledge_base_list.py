from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .knowledge_base import KnowledgeBase


@dataclass_json
@dataclass(frozen=True)
class KnowledgeBasesList:
    """KnowledgeBasesList contains the list of your knowledge bases."""

    knowledge_bases: List[KnowledgeBase]


def list_knowledge_bases(*, client: HttpClient) -> KnowledgeBasesList:
    """list_knowledge_bases returns all of your knowledge bases.

    Note: requires an `Integration` or `Management` API key."""
    rsp = client.get(path="knowledge-bases")
    return KnowledgeBasesList.from_dict(rsp)
