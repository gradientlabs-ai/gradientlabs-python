from ._http_client import HttpClient
from ._without_none import without_none
from .tool import Tool, ToolUpdateParams


def update_tool(*, client: HttpClient, params: ToolUpdateParams) -> Tool:
    """Updates a webhook, HTTP, async or draft tool.

    Only draft tools can change kind. Edit repository-managed tools in their files.

    Note: requires a `Management` API key."""
    body = without_none(params.to_dict())
    body.pop("id")
    rsp = client.put(
        path=f"tools/{params.id}",
        body=body,
    )
    return Tool.from_dict(rsp)
