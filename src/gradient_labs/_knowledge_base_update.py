from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .knowledge_base import KnowledgeBase


@dataclass_json
@dataclass(frozen=True)
class UpdateKnowledgeBaseParams:
    """UpdateKnowledgeBaseParams contains the parameters for updating a knowledge base."""

    # name is the new name of the knowledge base.
    name: str


def update_knowledge_base(
    *, client: HttpClient, knowledge_base_id: str, params: UpdateKnowledgeBaseParams
) -> KnowledgeBase:
    """update_knowledge_base renames a knowledge base.

    Note: requires an `Integration` or `Management` API key."""
    rsp = client.post(
        path=f"knowledge-bases/{knowledge_base_id}", body=params.to_dict()
    )
    return KnowledgeBase.from_dict(rsp)
