from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ._datetime import datetime_config


@dataclass_json
@dataclass(frozen=True)
class KnowledgeBase:
    """KnowledgeBase groups articles and notes, and controls which AI agents can use them."""

    # gradient_labs_id is the internal Gradient Labs identifier for this knowledge base.
    gradient_labs_id: str

    # id is your own identifier for this knowledge base. Name the knowledge base by
    # this ID in `knowledge_base_ids` on articles and notes.
    id: str

    # name is the name of the knowledge base.
    name: str

    # created is when the knowledge base was created.
    created: datetime = field(metadata=datetime_config)

    # updated is when the knowledge base was last updated.
    updated: datetime = field(metadata=datetime_config)
