from typing import Optional, Dict, Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .terminology_substitution import TerminologySubstitution


@dataclass_json
@dataclass(frozen=True)
class TerminologySubstitutionUpdateParams:
    blocked: str
    blocked_description: str
    replacement: str
    resource_type_id: Optional[str] = None
    resource_attribute_json_path: Optional[str] = None
    resource_value_to_match: Optional[str] = None


def update_terminology_substitution(
    *,
    client: HttpClient,
    substitution_id: str,
    params: TerminologySubstitutionUpdateParams,
) -> TerminologySubstitution:
    body: Dict[str, Any] = {
        "blocked": params.blocked,
        "blocked_description": params.blocked_description,
        "replacement": params.replacement,
    }
    if params.resource_type_id is not None:
        body["resource_type_id"] = params.resource_type_id
    if params.resource_attribute_json_path is not None:
        body["resource_attribute_json_path"] = params.resource_attribute_json_path
    if params.resource_value_to_match is not None:
        body["resource_value_to_match"] = params.resource_value_to_match
    rsp = client.put(path=f"terminology-substitutions/{substitution_id}", body=body)
    return TerminologySubstitution.from_dict(rsp)
