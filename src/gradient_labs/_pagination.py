from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class ForwardPaginationInfo:
    # next is a cursor to retrieve the next page of results.
    next: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class PaginationInfo(ForwardPaginationInfo):
    prev: Optional[str] = None
