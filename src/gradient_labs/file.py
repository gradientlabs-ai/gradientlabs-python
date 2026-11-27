from typing import Dict
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ._datetime import datetime_config


@dataclass_json
@dataclass(frozen=True)
class FileUpload:
    """FileUpload tells you where to send a file's contents."""

    # upload_id identifies the upload. Pass it to create_file once the file has
    # been uploaded.
    upload_id: str

    # upload_url is where to send the file, as an HTTP `PUT` with every header in headers.
    upload_url: str

    # content_type is the `Content-Type` header the `PUT` must send.
    content_type: str

    # headers are every header the `PUT` must send, `Content-Type` included.
    headers: Dict[str, str]

    # expires_at is when upload_url stops accepting the file.
    expires_at: datetime = field(metadata=datetime_config)

    # max_bytes is the largest file that can be uploaded, in bytes.
    max_bytes: int


@dataclass_json
@dataclass(frozen=True)
class File:
    """File is a file your company has uploaded."""

    # id is the file's unique identifier.
    id: str

    # ref is the file's name in a back-office test case, which lists it as `file_ref`.
    # It never changes.
    ref: str

    # file_name is the name the file was uploaded with, which the AI agent sees.
    file_name: str

    # content_type is the file's type, read from its contents.
    content_type: str

    # size_bytes is the file's size in bytes.
    size_bytes: int

    # created is when the file was uploaded.
    created: datetime = field(metadata=datetime_config)
