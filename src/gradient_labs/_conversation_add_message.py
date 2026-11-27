from typing import Optional, List
from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .conversation import Attachment, ParticipantType
from ._datetime import optional_datetime_config
from ._without_none import without_none


@dataclass_json
@dataclass(frozen=True)
class AddMessageParams:
    # id uniquely identifies this message within the conversation.
    #
    # Can be anything consisting of letters, numbers, or any of the following
    # characters: _ - + =.
    #
    # Tip: use something meaningful to your business.
    id: str

    # body contains the message text.
    body: Optional[str] = None

    # participant_id identifies the message sender.
    participant_id: Optional[str] = None

    # participant_type identifies the type of participant who sent this message.
    # Use AI_AGENT only to replay a message already sent by the AI agent.
    participant_type: Optional[ParticipantType] = None

    # created is the time at which the message was sent.
    created: Optional[datetime] = None

    # attachments contains any files that were uploaded with this message.
    attachments: Optional[List[Attachment]] = None

    # conversation_token is the raw sensitive token that can be optionally provided in every message.
    # The latest token of the conversation will be echoed back in future Webhooks, under the header `X-GradientLabs-Token`,
    # as well as in HTTP Tools using templates.
    conversation_token: Optional[str] = None

    # subject is the email subject line. It is only valid for email conversations,
    # and rejected for every other channel.
    subject: Optional[str] = None

    def __post_init__(self):
        if self.participant_type is None:
            raise TypeError("participant_type is required")


@dataclass_json
@dataclass(frozen=True)
class Message:
    # id uniquely identifies this message within the conversation.
    #
    # Can be anything consisting of letters, numbers, or any of the following
    # characters: _ - + =.
    #
    # Tip: use something meaningful to your business.
    id: str

    # body contains the message text.
    body: str

    # participant_type identifies the type of participant who sent this message.
    participant_type: ParticipantType

    participant_id: str
    created: Optional[datetime] = field(default=None, metadata=optional_datetime_config)
    attachments: Optional[List[Attachment]] = None


def add_message(
    *, client: HttpClient, conversation_id: str, params: AddMessageParams
) -> Message:
    body = {
        "id": params.id,
        "participant_type": params.participant_type.value,
    }
    if params.body is not None:
        body["body"] = params.body
    if params.participant_id is not None:
        body["participant_id"] = params.participant_id
    if params.created is not None:
        body["created"] = HttpClient.localize(params.created)
    if params.attachments is not None:
        body["attachments"] = [without_none(a.to_dict()) for a in params.attachments]
    if params.conversation_token is not None:
        body["conversation_token"] = params.conversation_token
    if params.subject is not None:
        body["subject"] = params.subject

    rsp = client.post(path=f"conversations/{conversation_id}/messages", body=body)
    return Message.from_dict(rsp)
