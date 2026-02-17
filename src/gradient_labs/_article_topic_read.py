from typing import Optional
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .topic import Topic
from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class ReadTopicParams:
    """Parameters for reading a topic."""

    # support_platform specifies which platform's topic to read.
    # Valid values include "public-api" and "intercom". If not provided,
    # defaults to "public-api". This allows reading topics from
    # different support platforms within the same organization.
    support_platform: Optional[str] = None


def read_topic(
    *, client: HttpClient, topic_id: str, params: Optional[ReadTopicParams] = None
) -> Topic:
    """read_topic reads an article topic by ID.

    Note: requires a `Management` API key."""
    query_params = {}
    if params and params.support_platform:
        query_params["support_platform"] = params.support_platform

    response = client.get(path=f"topic/{topic_id}", query_params=query_params)
    return Topic.from_dict(response)
