from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .knowledge_base import KnowledgeBase


@dataclass_json
@dataclass(frozen=True)
class CreateKnowledgeBaseParams:
    """CreateKnowledgeBaseParams contains the parameters for creating a knowledge base."""

    # id is your own identifier for this knowledge base.
    id: str

    # name is the name of the knowledge base.
    name: str


def create_knowledge_base(
    *, client: HttpClient, params: CreateKnowledgeBaseParams
) -> KnowledgeBase:
    """create_knowledge_base creates a new knowledge base.

    Note: requires an `Integration` or `Management` API key."""
    rsp = client.post(path="knowledge-bases", body=params.to_dict())
    return KnowledgeBase.from_dict(rsp)
