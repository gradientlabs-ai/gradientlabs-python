from ._http_client import HttpClient
from ._without_none import without_none
from .tool import Tool


def create_tool(*, client: HttpClient, params: Tool) -> Tool:
    """create_tool creates a new tool.

    Note: requires a `Management` API key."""
    body = without_none(params.to_dict())
    body.pop("id", None)
    body.pop("mcp", None)
    rsp = client.post(path="tools", body=body)
    return Tool.from_dict(rsp)
