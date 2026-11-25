from typing import List, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from ._pagination import ForwardPaginationInfo
from .file import File


@dataclass_json
@dataclass(frozen=True)
class FileListParams:
    """FileListParams contains the parameters for listing files."""

    # cursor is the page to fetch, from `pagination.next` in a previous response.
    # Leave it out to get the first page.
    cursor: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class FileListResponse:
    """FileListResponse is a page of files."""

    # files are your company's files on this page, newest first.
    files: List[File]

    # pagination contains the cursor for the next page, if there is one.
    pagination: ForwardPaginationInfo


def list_files(
    *, client: HttpClient, params: Optional[FileListParams] = None
) -> FileListResponse:
    """list_files returns a page of the files uploaded to your workspace.

    Note: requires a `Management` API key."""
    query_params = {}
    if params is not None and params.cursor is not None:
        query_params["cursor"] = params.cursor

    rsp = client.get(path="files", query_params=query_params)
    return FileListResponse.from_dict(rsp)
