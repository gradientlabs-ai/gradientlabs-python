from ._http_client import HttpClient
from .terminology_substitution import TerminologySubstitution


def read_terminology_substitution(
    *, client: HttpClient, substitution_id: str
) -> TerminologySubstitution:
    rsp = client.get(path=f"terminology-substitutions/{substitution_id}", body={})
    return TerminologySubstitution.from_dict(rsp)
