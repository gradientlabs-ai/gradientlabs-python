from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .file import FileUpload


@dataclass_json
@dataclass(frozen=True)
class BeginFileUploadParams:
    """BeginFileUploadParams contains the parameters for starting a file upload."""

    # content_type is the `Content-Type` header the upload sends. Leave it out to send
    # `application/octet-stream`: the file's type is read from its contents either way.
    content_type: Optional[str] = None


def begin_file_upload(
    *, client: HttpClient, params: Optional[BeginFileUploadParams] = None
) -> FileUpload:
    """begin_file_upload starts uploading a file to your workspace. PUT the file to the
    returned upload_url, then call create_file with the upload_id.

    Note: requires a `Management` API key."""
    body = {}
    if params is not None and params.content_type is not None:
        body["content_type"] = params.content_type

    rsp = client.post(path="file-uploads", body=body)
    return FileUpload.from_dict(rsp)
