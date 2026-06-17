from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .voice_call_context import VoiceCallContext


@dataclass_json
@dataclass(frozen=True)
class VoiceCallContextReadParams:
    lookback_seconds: Optional[int] = None
    include_large_fields: Optional[bool] = None


def read_voice_call_context(
    *,
    client: HttpClient,
    phone_number: str,
    params: Optional[VoiceCallContextReadParams] = None,
) -> VoiceCallContext:
    path = f"voice/latest-call-context/{phone_number}"
    query_parts = []
    if params is not None:
        if params.lookback_seconds is not None:
            query_parts.append(f"lookback_seconds={params.lookback_seconds}")
        if params.include_large_fields is not None:
            query_parts.append(
                f"include_large_fields={str(params.include_large_fields).lower()}"
            )
    if query_parts:
        path = f"{path}?{'&'.join(query_parts)}"
    rsp = client.get(path=path, body={})
    return VoiceCallContext.from_dict(rsp)
