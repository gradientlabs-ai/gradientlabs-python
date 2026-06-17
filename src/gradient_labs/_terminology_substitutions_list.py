from typing import List

from ._http_client import HttpClient
from .terminology_substitution import TerminologySubstitution


def list_terminology_substitutions(
    *, client: HttpClient
) -> List[TerminologySubstitution]:
    rsp = client.get(path="terminology-substitutions", body={})
    return [TerminologySubstitution.from_dict(item) for item in rsp]
