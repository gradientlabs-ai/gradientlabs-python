from typing import Optional

from ._http_client import HttpClient
from .tool import Tool


def read_tool(
    *, client: HttpClient, tool_id: str, version: Optional[int] = None
) -> Tool:
    """Leave version out to read the current tool version.
    Enabled MCP tools can be read by ID. Interactive tools return 404.
    Note: requires a `Management` API key."""
    query_params = {}
    if version is not None:
        query_params["version"] = version

    rsp = client.get(
        path=f"tools/{tool_id}",
        query_params=query_params,
    )
    return Tool.from_dict(rsp)
