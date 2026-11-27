from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .file import File


@dataclass_json
@dataclass(frozen=True)
class CreateFileParams:
    """CreateFileParams contains the parameters for creating a file."""

    # upload_id is the `upload_id` that begin_file_upload returned.
    upload_id: str

    # file_name is the file's name, which the AI agent sees: 1 to 200 characters, with
    # no slashes and no space at either end.
    file_name: str

    # ref is the name a back-office test case uses to list this file as an attachment.
    # Leave it out to have one made from file_name.
    ref: Optional[str] = None


def create_file(*, client: HttpClient, params: CreateFileParams) -> File:
    """create_file turns an uploaded file into a workspace file. Calling it again with
    the same upload_id returns the same file.

    Note: requires a `Management` API key."""
    body = {
        "upload_id": params.upload_id,
        "file_name": params.file_name,
    }
    if params.ref is not None:
        body["ref"] = params.ref

    rsp = client.post(path="files", body=body)
    return File.from_dict(rsp)
