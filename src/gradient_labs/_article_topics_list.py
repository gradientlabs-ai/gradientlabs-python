from typing import List, Optional
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .topic import Topic
from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class ListTopicsParams:
    """Parameters for listing topics."""

    # support_platform optionally filters topics by support platform.
    # Valid values include "public-api" and "intercom". If not provided,
    # defaults to "public-api". This allows reading topics from
    # different support platforms within the same organization.
    support_platform: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class ListTopicsResponse:
    """Response containing a list of topics."""

    topics: List[Topic]


def list_topics(
    *, client: HttpClient, params: Optional[ListTopicsParams] = None
) -> ListTopicsResponse:
    """list_topics lists a company's topics, optionally filtered by support platform.

    Note: requires a `Management` API key."""
    query_params = {}
    if params and params.support_platform:
        query_params["support_platform"] = params.support_platform

    response = client.get(path="topics", query_params=query_params)
    return ListTopicsResponse.from_dict(response)
