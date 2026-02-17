from typing import Optional, Any, Dict
from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient


@dataclass_json
@dataclass(frozen=True)
class ReturnAsyncToolResultParams:
    """Parameters for returning an async tool execution result.

    When a tool is configured for asynchronous execution, the agent will request
    the tool execution via an action.execute webhook event, and your system should
    return the result using this method.
    """

    # async_tool_execution_id is the unique identifier for the async tool execution.
    # This ID is provided in the action.execute webhook event when the agent
    # requests the tool execution.
    async_tool_execution_id: str

    # payload is the result data from the tool execution as a JSON object.
    # The structure of this object depends on your tool's implementation.
    # The agent will use AI to extract relevant information from any well-formed
    # JSON object.
    payload: Dict[str, Any]

    # timestamp optionally defines the time when the result was generated.
    # If not given, this will default to the current time.
    timestamp: Optional[datetime] = None


def return_async_tool_result(
    *, client: HttpClient, conversation_id: str, params: ReturnAsyncToolResultParams
) -> None:
    """Returns the result of an async tool execution.

    When a tool is configured for asynchronous execution, the agent will request
    the tool execution via an action.execute webhook event, and your system should
    return the result by calling this function.

    This allows your system to perform long-running operations without blocking the
    conversation, and return results when they're ready.

    Important Notes:
    - The conversation must be in an ongoing state. You cannot return async tool
      results to conversations that are finished, failed, or cancelled.
    - Make sure to use the correct async_tool_execution_id from the action.execute
      webhook event.
    - The result payload should be a valid JSON object containing the data the
      agent needs to continue the conversation.
    """
    body = {
        "async_tool_execution_id": params.async_tool_execution_id,
        "payload": params.payload,
    }
    if params.timestamp:
        body["timestamp"] = client.localize(params.timestamp)

    _ = client.put(
        f"conversations/{conversation_id}/return-async-tool-result",
        body=body,
    )
