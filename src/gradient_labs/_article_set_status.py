from typing import Optional, Any
from collections import defaultdict
from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields

from .article import Visibility, PublicationStatus, ArticleUsageStatus
from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class SetArticleUsageStatusParams:
    usage_status: ArticleUsageStatus


def set_article_usage_status(
    *, client: HttpClient, id: str, params: SetArticleUsageStatusParams
) -> None:
    _ = client.post(
        path=f"articles/{id}/usage-status",
        body={"usage_status": params.usage_status.value},
    )
