from datetime import timedelta
from typing import Optional, List, Dict
from enum import Enum
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields


class ParameterType(str, Enum):
    """ParameterType determines the data type of a parameter."""

    # STRING indicates the parameter accepts string/text values.
    STRING: str = "string"

    # STRING_ARRAY indicates the parameter accepts a list of strings. The API only
    # returns it on existing tools: creating or updating a tool with it fails.
    STRING_ARRAY: str = "string_array"

    # JSON indicates the parameter accepts a JSON value. The API only returns it
    # on existing tools: creating or updating a tool with it fails.
    JSON: str = "json"

    # INTEGER indicates the parameter accepts whole numbers.
    INTEGER: str = "integer"

    # FLOAT indicates the parameter accepts decimal numbers.
    FLOAT: str = "float"

    # BOOLEAN indicates the parameter accepts true or false.
    BOOLEAN: str = "boolean"

    # DATE indicates the parameter accepts a calendar date.
    DATE: str = "date"

    # TIMESTAMP indicates the parameter accepts a date and time.
    TIMESTAMP: str = "timestamp"

    # DURATION indicates the parameter accepts a length of time.
    DURATION: str = "duration"

    # ATTACHMENT indicates the parameter accepts a file. Set transfer_mode too.
    ATTACHMENT: str = "attachment"


class ParameterSource(str, Enum):
    """ParameterSource says where a parameter's value can come from."""

    # LLM means the AI agent provides the value.
    LLM: str = "llm"

    # LITERAL means a procedure sets a fixed value.
    LITERAL: str = "literal"

    # RESOURCE means the value comes from a resource.
    RESOURCE: str = "resource"


class TransferMode(str, Enum):
    """TransferMode says how an attachment parameter's file reaches the tool."""

    # BASE64 sends the file's contents, base64-encoded.
    BASE64: str = "base64"

    # TEMPORARY_URL sends a temporary URL to download the file from.
    TEMPORARY_URL: str = "temporary_url"


class BodyEncoding(str, Enum):
    """BodyEncoding determines how the HTTP body will be encoded."""

    # FORM indicates the body will be encoded using URL encoding.
    FORM: str = "application/x-www-form-urlencoded"

    # JSON indicates the body will be encoded as JSON.
    JSON: str = "application/json"


@dataclass_json
@dataclass
class ParameterOption:
    value: str
    text: str


@dataclass_json
@dataclass(frozen=True)
class ToolParameter:
    name: str
    description: str
    type: ParameterType
    required: Optional[bool] = False
    options: Optional[List[ParameterOption]] = field(default_factory=lambda: [])

    # allowed_sources says where the parameter's value can come from. At least
    # one is required.
    allowed_sources: List[ParameterSource] = field(
        default_factory=lambda: [ParameterSource.LLM]
    )

    # transfer_mode says how an attachment parameter's file reaches the tool. It is
    # required when type is ATTACHMENT, and not allowed for any other type.
    transfer_mode: Optional[TransferMode] = None


@dataclass_json
@dataclass(frozen=True)
class ToolParameterSet:
    """ToolParameterSet is a group of parameters that apply when a discriminator
    parameter has a given value."""

    # discriminator_parameter_name is the name of the top-level parameter whose
    # value decides whether this set applies.
    discriminator_parameter_name: str

    # discriminator_value is the value of that parameter that activates this set.
    discriminator_value: str

    # parameters are the extra parameters that apply when this set is active.
    parameters: List[ToolParameter]


@dataclass_json
@dataclass(frozen=True)
class ToolWebhookConfiguration:
    name: str


@dataclass_json
@dataclass(frozen=True)
class HTTPRetryDefinition:
    """HTTPRetryDefinition overrides how a tool's HTTP request is retried."""

    # max_attempts is the most times the request is tried.
    max_attempts: Optional[int] = None

    # request_timeout_seconds is how long each attempt may take.
    request_timeout_seconds: Optional[int] = None


@dataclass_json
@dataclass(frozen=True)
class HTTPBodyDefinition:
    encoding: BodyEncoding
    json_template: Optional[str] = ""
    form_field_templates: Optional[Dict[str, str]] = None


@dataclass_json
@dataclass(frozen=True)
class HTTPDefinition:
    method: str
    url_template: str
    header_templates: Optional[Dict[str, str]] = None
    body: Optional[HTTPBodyDefinition] = None
    retry: Optional[HTTPRetryDefinition] = None


@dataclass_json
@dataclass(frozen=True)
class AsyncChildTool:
    """AsyncChildTool is one step of an async tool. It uses its parent tool's parameters.
    Set either webhook or http."""

    webhook: Optional[ToolWebhookConfiguration] = None
    http: Optional[HTTPDefinition] = None


def _encode_timeout(value: timedelta) -> int:
    return (value // timedelta(microseconds=1)) * 1000


def _decode_timeout(value: int) -> timedelta:
    return timedelta(microseconds=value // 1000)


@dataclass_json
@dataclass(frozen=True)
class AsyncDefinition:
    """AsyncDefinition configures a tool for long-running operations."""

    # start_execution_tool starts the operation. It runs as soon as the tool is used.
    start_execution_tool: AsyncChildTool

    # timeout is the longest to wait for the operation to finish.
    timeout: timedelta = field(
        metadata=config(
            encoder=_encode_timeout,
            decoder=_decode_timeout,
            mm_field=fields.TimeDelta(),
        )
    )

    # cancel_execution_tool optionally cancels the operation.
    cancel_execution_tool: Optional[AsyncChildTool] = None


@dataclass_json
@dataclass(frozen=True)
class ToolMCPConfiguration:
    """ToolMCPConfiguration runs a tool on a Model Context Protocol server. The API
    only returns it when reading a tool: creating a tool with it fails."""

    server_id: str
    external_tool_name: str


@dataclass_json
@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    id: Optional[str] = None
    parameters: List[ToolParameter] = field(default_factory=lambda: [])
    webhook: Optional[ToolWebhookConfiguration] = None
    http: Optional[HTTPDefinition] = None

    # parameter_sets are groups of extra parameters that apply when a discriminator
    # parameter has a given value.
    parameter_sets: Optional[List[ToolParameterSet]] = None

    # async_ configures a long-running tool. It is sent as `async`.
    async_: Optional[AsyncDefinition] = field(
        default=None, metadata=config(field_name="async")
    )

    # mcp is set on tools that run on an MCP server.
    mcp: Optional[ToolMCPConfiguration] = None

    # draft marks a tool that is still being built. A draft tool cannot run, and
    # takes no webhook, http or async configuration.
    draft: Optional[bool] = None

    # branch_id is the ID of the git-backed branch to create the tool on. Only used
    # when creating a tool: send this or branch_name.
    branch_id: Optional[str] = None

    # branch_name is the name of the git-backed branch to create the tool on, as an
    # alternative to branch_id. Only used when creating a tool.
    branch_name: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class ToolUpdateParams:
    id: str
    description: Optional[str] = None
    parameters: Optional[List[ToolParameter]] = None
    webhook: Optional[ToolWebhookConfiguration] = None
    http: Optional[HTTPDefinition] = None

    # parameter_sets are groups of extra parameters that apply when a discriminator
    # parameter has a given value.
    parameter_sets: Optional[List[ToolParameterSet]] = None

    # async_ configures a long-running tool. It is sent as `async`.
    async_: Optional[AsyncDefinition] = field(
        default=None, metadata=config(field_name="async")
    )
