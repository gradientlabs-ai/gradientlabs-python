from typing import Optional, Any, List
from collections import defaultdict
from datetime import datetime

from ._datetime import parse_datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .article import Visibility, PublicationStatus
from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class UpsertArticleParams:
    # id is your identifier of choice for this article.
    id: str

    # visibility describes who can access this article, ranging from the
    # whole world (public) through to employees only (internal).
    visibility: Visibility

    # status describes whether this article is published or not.
    status: PublicationStatus

    # created is when the article was first created.
    created: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # last_edited is when the article was last changed.
    last_edited: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=parse_datetime,
            mm_field=fields.DateTime(format="iso"),
        )
    )

    # topic_id optionally identifies the topic that this
    # article is associated with. If given, you must have created
    # the topic first (see: UpsertArticleTopic)
    topic_id: Optional[str] = None

    # author_id optionally identifies the user who last edited the article
    author_id: Optional[str] = None

    # title is the article's title. It may be empty if the article is a draft.
    title: Optional[str] = None

    # description is an article's tagline. It may be empty.
    description: Optional[str] = None

    # body is the main contents of an article. It may be empty if the article is a draft.
    body: Optional[str] = None

    # data optionally gives additional meta-data about the article.
    data: Optional[Any] = field(default_factory=lambda: defaultdict(dict))

    # public_url optionally links to where the article can be read online.
    public_url: Optional[str] = None

    # knowledge_base_ids optionally names the knowledge bases this article belongs to.
    # Use the IDs of knowledge bases you created with create_knowledge_base, or
    # "public-api". The list cannot be empty. If you leave it out, the article goes
    # into the default "public-api" knowledge base, replacing any others it was in.
    knowledge_base_ids: Optional[List[str]] = None


def upsert_article(*, client: HttpClient, params: UpsertArticleParams) -> None:
    body = params.to_dict()
    if params.title is None:
        body.pop("title")
    if params.description is None:
        body.pop("description")
    if params.topic_id is None:
        body.pop("topic_id")
    if params.author_id is None:
        body.pop("author_id")
    if params.body is None:
        body.pop("body")
    if params.public_url is None:
        body.pop("public_url")
    if params.knowledge_base_ids is None:
        body.pop("knowledge_base_ids")

    body["created"] = HttpClient.localize(params.created)
    body["last_edited"] = HttpClient.localize(params.last_edited)
    _ = client.post(
        path="articles",
        body=body,
    )
