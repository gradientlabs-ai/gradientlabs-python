from typing import Optional, List

from ._article_delete import delete_article
from ._article_set_status import set_article_usage_status, SetArticleUsageStatusParams
from ._article_topic_upsert import upsert_article_topic, ArticleTopicUpsertParams
from ._article_topic_read import read_topic, ReadTopicParams
from ._article_topics_list import list_topics, ListTopicsParams, ListTopicsResponse
from ._article_upsert import upsert_article, UpsertArticleParams

from .topic import Topic

from .conversation import Conversation
from ._conversation_add_message import add_message, AddMessageParams, Message
from ._conversation_assign import assign_conversation, AssignmentParams
from ._conversation_cancel import cancel_conversation, CancelParams
from ._conversation_event import add_conversation_event, EventParams
from ._conversation_finish import finish_conversation, FinishParams
from ._conversation_rate import rate_conversation, RatingParams
from ._conversation_resume import resume_conversation, ResumeParams
from ._conversation_read import read_conversation, ReadParams
from ._conversation_start import start_conversation, StartConversationParams
from ._conversation_return_async_tool_result import (
    return_async_tool_result,
    ReturnAsyncToolResultParams,
)

from ._outbound_conversation_start import (
    start_outbound_conversation,
    StartOutboundConversationParams,
    StartOutboundConversationResponse,
)

from ._handoff_target_upsert import upsert_hand_off_target, UpsertHandOffTargetParams
from ._handoff_targets import list_handoff_targets, HandOffTargets
from ._handoff_target_delete import delete_hand_off_target, DeleteHandOffTargetParams
from ._handoff_target_set_default import (
    set_default_hand_off_target,
    SetDefaultHandOffTargetParams,
)
from ._handoff_target_get_default import (
    get_default_hand_off_target,
    GetDefaultHandOffTargetParams,
    GetDefaultHandOffTargetResponse,
)

from .procedure import Procedure
from ._procedure_read import read_procedure
from ._procedure_list import list_procedures, ProcedureListParams, ProcedureListResponse
from ._procedure_set_limit import set_procedure_limit, ProcedureLimitParams
from ._procedure_version_list import (
    list_procedure_versions,
    ListProcedureVersionsResponse,
)
from ._procedure_version_live_set import set_procedure_live_version
from ._procedure_version_live_unset import unset_procedure_live_version
from ._procedure_version_gated_set import (
    set_procedure_gated_version,
    SetProcedureGatedVersionParams,
)
from ._procedure_version_gated_unset import unset_procedure_gated_version

from ._tool_create import create_tool
from ._tool_delete import delete_tool
from ._tool_execute import execute_tool, ToolExecuteParams, ToolExecuteResult
from ._tool_list import list_tools
from ._tool_read import read_tool
from ._tool_update import update_tool

from ._note_create import create_note, CreateNoteParams
from ._note_delete import delete_note
from ._note_update import update_note, UpdateNoteParams
from ._note_set_status import set_note_status, SetNoteStatusParams

from ._secret_write import write_secret, WriteSecretParams
from ._secrets_list import list_secrets, SecretsList
from ._secret_revoke import revoke_secret

from ._resource_type_create import create_resource_type, CreateResourceTypeParams
from ._resource_type_list import list_resource_types, ResourceTypesList
from ._resource_type_read import read_resource_type
from ._resource_type_update import update_resource_type, UpdateResourceTypeParams
from ._resource_type_delete import delete_resource_type

from ._resource_source_create import create_resource_source, CreateResourceSourceParams
from ._resource_source_list import list_resource_sources, ResourceSourcesList
from ._resource_source_read import read_resource_source
from ._resource_source_update import update_resource_source, UpdateResourceSourceParams
from ._resource_source_update_schema_by_examples import (
    update_resource_source_schema_by_examples,
    UpdateResourceSourceSchemaByExamplesParams,
)
from ._resource_source_delete import delete_resource_source

from .traffic_group import TrafficGroup, TrafficGroupTarget
from ._traffic_group_create import create_traffic_group, CreateTrafficGroupParams
from ._traffic_group_list import list_traffic_groups, TrafficGroupsList
from ._traffic_group_update import update_traffic_group, UpdateTrafficGroupParams
from ._traffic_group_delete import delete_traffic_group
from ._traffic_group_target_create import (
    create_traffic_group_target,
    CreateTrafficGroupTargetParams,
)
from ._traffic_group_target_delete import delete_traffic_group_target

from ._voice_call_context_read import (
    read_voice_call_context,
    VoiceCallContextReadParams,
)
from .voice_call_context import VoiceCallContext

from .back_office_task import (
    BackOfficeTask,
)
from ._back_office_task_create import (
    create_back_office_task,
    BackOfficeTaskCreateParams,
    BackOfficeTaskCreateAttachment as BackOfficeTaskCreateAttachment,
)
from ._back_office_task_read import read_back_office_task

from .terminology_substitution import TerminologySubstitution
from ._terminology_substitution_create import (
    create_terminology_substitution,
    TerminologySubstitutionCreateParams,
)
from ._terminology_substitutions_list import list_terminology_substitutions
from ._terminology_substitution_read import read_terminology_substitution
from ._terminology_substitution_update import (
    update_terminology_substitution,
    TerminologySubstitutionUpdateParams,
)
from ._terminology_substitution_delete import delete_terminology_substitution

from ._traffic_group_exclusion_create import (
    create_traffic_group_exclusion,
    TrafficGroupExclusionCreateParams,
)
from ._traffic_group_exclusion_delete import delete_traffic_group_exclusion

from .ip_addresses import IPAddresses
from ._ip_addresses_list import list_ip_addresses

from ._http_client import HttpClient, API_BASE_URL
from .tool import *
from .note import Note
from .secret import Secret
from .resource_type import ResourceType
from .resource_source import (
    ResourceSource,
)
from .webhook import Webhook, WebhookEvent


class Client:
    """Client is the client for the Gradient Labs
    public api. For full details, please refer to the online docs:

    https://api-docs.gradient-labs.ai/
    """

    def __init__(
        self,
        *,
        api_key: str,
        signing_key: Optional[str] = None,
        base_url: Optional[str] = API_BASE_URL,
        timeout: Optional[int] = None,
    ):
        self.http_client = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.signing_key = signing_key

    def delete_article(self, *, id: str) -> None:
        """delete_article marks an article as deleted. Copies of the article are kept
        in case they are needed to render citations."""
        delete_article(
            client=self.http_client,
            id=id,
        )

    def set_article_usage_status(
        self, *, id: str, params: SetArticleUsageStatusParams
    ) -> None:
        """set_article_usage_status updates an article's usage status. Use this to
        make it (un)available for use by the AI agent."""
        set_article_usage_status(
            client=self.http_client,
            id=id,
            params=params,
        )

    def upsert_article_topic(self, *, params: ArticleTopicUpsertParams) -> None:
        """upsert_article_topic inserts or updates a help article topic"""
        upsert_article_topic(
            client=self.http_client,
            params=params,
        )

    def upsert_article(self, *, params: UpsertArticleParams) -> None:
        """upsert_article inserts or updates a help article"""
        upsert_article(
            client=self.http_client,
            params=params,
        )

    def list_topics(
        self, *, params: Optional[ListTopicsParams] = None
    ) -> ListTopicsResponse:
        """list_topics lists a company's topics, optionally filtered by support platform.

        Note: requires a `Management` API key."""
        return list_topics(
            client=self.http_client,
            params=params,
        )

    def read_topic(
        self, *, topic_id: str, params: Optional[ReadTopicParams] = None
    ) -> Topic:
        """read_topic reads an article topic by ID.

        Note: requires a `Management` API key."""
        return read_topic(
            client=self.http_client,
            topic_id=topic_id,
            params=params,
        )

    def assign_conversation(
        self,
        *,
        conversation_id: str,
        params: AssignmentParams,
    ) -> None:
        """Assigns a conversation to the given participant."""
        assign_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def cancel_conversation(
        self, *, conversation_id: str, params: CancelParams
    ) -> None:
        """cancel_conversation cancels the conversation.

        This is intended for cases where the conversation is being explicitly cancelled or terminated.
        Use finish_conversation() when the conversation is has reached a natural 'end' state, such as it being
        resolved or closed due to inactivity."""
        cancel_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def add_conversation_event(
        self, *, conversation_id: str, params: EventParams
    ) -> None:
        """add_conversation_event records an event, such as the customer started typing."""
        add_conversation_event(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def finish_conversation(
        self,
        *,
        conversation_id: str,
        params: FinishParams,
    ) -> None:
        """finish_conversation finishes a conversation.

        A conversation finishes when it has come to its natural conclusion. This could be because
        the customer's query has been resolved, a human agent or other automation has closed the chat,
        or because the chat is being closed due to inactivity."""
        finish_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def rate_conversation(self, *, conversation_id: str, params: RatingParams) -> None:
        """rate_conversation submits a customer (CSAT) rating for a conversation."""
        rate_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def resume_conversation(
        self, *, conversation_id: str, params: ResumeParams
    ) -> None:
        """resume_conversation re-opens a conversation that was previously finished."""
        resume_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def read_conversation(
        self, *, conversation_id: str, params: Optional[ReadParams] = None
    ) -> Conversation:
        """Retrieves the conversation"""
        return read_conversation(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def start_conversation(
        self,
        *,
        params: StartConversationParams,
    ) -> Conversation:
        """Starts a conversation."""
        return start_conversation(
            client=self.http_client,
            params=params,
        )

    def start_outbound_conversation(
        self,
        *,
        params: StartOutboundConversationParams,
    ) -> StartOutboundConversationResponse:
        """Starts an outbound conversation.

        Creates and starts a new outbound conversation where the AI agent proactively
        initiates contact with a customer. The conversation follows the instructions
        defined in the specified outbound procedure.

        If support_platform is not provided, the system will automatically select the
        highest priority platform that has integration settings configured for your company.

        If body and subject are provided, that message will be sent as the initial message.
        Otherwise, the AI agent will generate an appropriate initial message based on the procedure."""
        return start_outbound_conversation(
            client=self.http_client,
            params=params,
        )

    def add_message(
        self,
        *,
        conversation_id: str,
        params: AddMessageParams,
    ) -> Message:
        """Adds a message to a conversation."""
        return add_message(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def return_async_tool_result(
        self,
        *,
        conversation_id: str,
        params: ReturnAsyncToolResultParams,
    ) -> None:
        """Returns the result of an async tool execution.

        When a tool is configured for asynchronous execution, the agent will request
        the tool execution via an action.execute webhook event, and your system should
        return the result by calling this method.

        This allows your system to perform long-running operations without blocking the
        conversation, and return results when they're ready."""
        return_async_tool_result(
            client=self.http_client,
            conversation_id=conversation_id,
            params=params,
        )

    def upsert_hand_off_target(self, *, params: UpsertHandOffTargetParams) -> None:
        """upsert_hand_off_target inserts or updates a hand-off target.

        Note: requires a `Management` API key."""
        upsert_hand_off_target(
            client=self.http_client,
            params=params,
        )

    def set_default_hand_off_target(
        self, *, params: SetDefaultHandOffTargetParams
    ) -> None:
        """set_default_hand_off_target sets the default hand-off target that the AI agent will
        use when handing off the conversation, if there is no specific target for that intent
        or procedure. This can be set by channel.

        Note: requires a `Management` API key."""
        set_default_hand_off_target(
            client=self.http_client,
            params=params,
        )

    def get_default_hand_off_target(
        self, *, params: GetDefaultHandOffTargetParams
    ) -> GetDefaultHandOffTargetResponse:
        """get_default_hand_off_target gets the current default hand-off target for the company.
        This can be retrieved by channel.

        Note: requires a `Management` API key."""
        return get_default_hand_off_target(
            client=self.http_client,
            params=params,
        )

    def delete_hand_off_target(self, *, params: DeleteHandOffTargetParams) -> None:
        """delete_hand_off_target deletes a hand-off target. This will fail if the hand off target
        is in use - either in a procedure, or in an intent.

        Note: requires a `Management` API key."""
        delete_hand_off_target(
            client=self.http_client,
            params=params,
        )

    def list_handoff_targets(self) -> HandOffTargets:
        """list_handoff_targets returns all of your hand off targets.

        Note: requires a `Management` API key."""
        return list_handoff_targets(client=self.http_client)

    def read_procedure(self, *, procedure_id: str) -> Procedure:
        """read_procedure reads a procedure.

        Note: requires a `Management` API key."""
        return read_procedure(
            client=self.http_client,
            procedure_id=procedure_id,
        )

    def list_procedures(self, *, params: ProcedureListParams) -> ProcedureListResponse:
        """list_procedures lists procedures.

        Note: requires a `Management` API key."""
        return list_procedures(
            client=self.http_client,
            params=params,
        )

    def set_procedure_limit(
        self, *, procedure_id: str, params: ProcedureLimitParams
    ) -> Procedure:
        """set_procedure_limit updates the daily usage limit of a procedure.

        Note: requires a `Management` API key."""
        return set_procedure_limit(
            client=self.http_client,
            procedure_id=procedure_id,
            params=params,
        )

    def list_procedure_versions(
        self, *, procedure_id: str
    ) -> ListProcedureVersionsResponse:
        """list_procedure_versions lists existing non-ephemeral versions of a procedure.

        Each procedure can have multiple versions, with one marked as "live" (production)
        and optionally one marked as "gated" for controlled testing.

        Note: requires a `Management` API key."""
        return list_procedure_versions(
            client=self.http_client,
            procedure_id=procedure_id,
        )

    def set_procedure_live_version(self, *, procedure_id: str, version: int) -> None:
        """set_procedure_live_version promotes a specific version to be the live (production) version.

        The live version is the default version used by the agent when no gated
        versions are active. If the specified version is currently marked as gated,
        the version will be promoted to live and will no longer be considered gated.

        Note: requires a `Management` API key."""
        set_procedure_live_version(
            client=self.http_client,
            procedure_id=procedure_id,
            version=version,
        )

    def unset_procedure_live_version(self, *, procedure_id: str, version: int) -> None:
        """unset_procedure_live_version removes the specified version from being the live revision.

        Once unset, the version will no longer be used by default by the agent.
        Unsetting the live version does not delete the version or affect the gated status (if any).

        Note: requires a `Management` API key."""
        unset_procedure_live_version(
            client=self.http_client,
            procedure_id=procedure_id,
            version=version,
        )

    def set_procedure_gated_version(
        self,
        *,
        procedure_id: str,
        version: int,
        params: SetProcedureGatedVersionParams,
    ) -> None:
        """set_procedure_gated_version marks a version as gated for A/B testing.

        Gated versions are served to a limited number of conversations per day.
        If a gated version already exists, the gated version will only be replaced
        if the 'replace' flag is set to True.

        Note: requires a `Management` API key."""
        set_procedure_gated_version(
            client=self.http_client,
            procedure_id=procedure_id,
            version=version,
            params=params,
        )

    def unset_procedure_gated_version(self, *, procedure_id: str, version: int) -> None:
        """unset_procedure_gated_version removes gated status from a version.

        Once unset, the version will no longer be used for A/B testing or served as a gated version.

        Note: requires a `Management` API key."""
        unset_procedure_gated_version(
            client=self.http_client,
            procedure_id=procedure_id,
            version=version,
        )

    def create_tool(self, *, tool: Tool) -> Tool:
        """create_tool creates a new tool.

        Note: requires a `Management` API key."""
        return create_tool(
            client=self.http_client,
            params=tool,
        )

    def delete_tool(self, *, tool_id: str):
        """delete_tool deletes a tool. Note: will not allow to delete a tool used in an active procedure.

        Note: requires a `Management` API key."""
        delete_tool(
            client=self.http_client,
            tool_id=tool_id,
        )

    def execute_tool(self, *, params: ToolExecuteParams) -> ToolExecuteResult:
        """execute_tool executes a tool.

        Note: requires a `Management` API key."""
        return execute_tool(
            client=self.http_client,
            params=params,
        )

    def read_tool(self, *, tool_id: str) -> Tool:
        """read_tool retrieves a new tool.

        Note: requires a `Management` API key."""
        return read_tool(
            client=self.http_client,
            tool_id=tool_id,
        )

    def list_tools(self) -> List[Tool]:
        """list_tools lists all tools.

        Note: requires a `Management` API key."""
        return list_tools(
            client=self.http_client,
        )

    def update_tool(self, *, params: ToolUpdateParams) -> Tool:
        """update_tool updates an existing tool. It allows callers to convert mock tools
        into real tools, but not the other way around.

        Note: requires a `Management` API key."""
        return update_tool(
            client=self.http_client,
            params=params,
        )

    def parse_webhook(self, payload: str, signature_header: str) -> WebhookEvent:
        """parse_webhook parses a webhook event."""
        return Webhook.parse_event(
            payload=payload,
            signature_header=signature_header,
            signing_key=self.signing_key,
        )

    def create_note(self, *, params: CreateNoteParams) -> Note:
        """create_note creates a new note."""
        return create_note(
            client=self.http_client,
            params=params,
        )

    def update_note(self, *, note_id: str, params: UpdateNoteParams) -> Note:
        """update_note updates an existing note's contents."""
        return update_note(
            client=self.http_client,
            note_id=note_id,
            params=params,
        )

    def delete_note(self, *, note_id: str) -> None:
        """delete_note marks a note as deleted."""
        delete_note(
            client=self.http_client,
            note_id=note_id,
        )

    def set_note_status(self, *, note_id: str, params: SetNoteStatusParams) -> None:
        """set_note_status updates a note's status."""
        set_note_status(
            client=self.http_client,
            note_id=note_id,
            params=params,
        )

    # Secret Operations

    def write_secret(self, *, params: WriteSecretParams) -> Secret:
        """write_secret creates or updates a secret. If a secret with the given name already exists,
        it will be updated with the new value and configuration.

        Note: requires a `Management` API key."""
        return write_secret(
            client=self.http_client,
            params=params,
        )

    def list_secrets(self) -> SecretsList:
        """list_secrets returns all of your secrets.

        Note: requires a `Management` API key."""
        return list_secrets(client=self.http_client)

    def revoke_secret(self, *, name: str) -> None:
        """revoke_secret permanently deletes a secret. This action cannot be undone.

        Note: requires a `Management` API key."""
        revoke_secret(
            client=self.http_client,
            name=name,
        )

    # Resource Type Operations

    def create_resource_type(self, *, params: CreateResourceTypeParams) -> ResourceType:
        """create_resource_type creates a new resource type.

        Note: requires a `Management` API key."""
        return create_resource_type(
            client=self.http_client,
            params=params,
        )

    def list_resource_types(self) -> ResourceTypesList:
        """list_resource_types returns all of your resource types.

        Note: requires a `Management` API key."""
        return list_resource_types(client=self.http_client)

    def read_resource_type(self, *, id: str) -> ResourceType:
        """read_resource_type retrieves a specific resource type by ID.

        Note: requires a `Management` API key."""
        return read_resource_type(
            client=self.http_client,
            id=id,
        )

    def update_resource_type(
        self, *, id: str, params: UpdateResourceTypeParams
    ) -> ResourceType:
        """update_resource_type updates an existing resource type.

        Note: requires a `Management` API key."""
        return update_resource_type(
            client=self.http_client,
            id=id,
            params=params,
        )

    def delete_resource_type(self, *, id: str) -> None:
        """delete_resource_type permanently deletes a resource type. This action cannot be undone.

        Note: requires a `Management` API key."""
        delete_resource_type(
            client=self.http_client,
            id=id,
        )

    # ==================== Resource Source Operations ====================

    def create_resource_source(
        self, *, params: CreateResourceSourceParams
    ) -> ResourceSource:
        """create_resource_source creates a new resource source.

        Note: requires a `Management` API key."""
        return create_resource_source(
            client=self.http_client,
            params=params,
        )

    def list_resource_sources(self) -> ResourceSourcesList:
        """list_resource_sources returns all of your resource sources.

        Note: requires a `Management` API key."""
        return list_resource_sources(client=self.http_client)

    def read_resource_source(self, *, id: str) -> ResourceSource:
        """read_resource_source retrieves a specific resource source by ID.

        Note: requires a `Management` API key."""
        return read_resource_source(
            client=self.http_client,
            id=id,
        )

    def update_resource_source(
        self, *, id: str, params: UpdateResourceSourceParams
    ) -> ResourceSource:
        """update_resource_source updates an existing resource source.

        Note: requires a `Management` API key."""
        return update_resource_source(
            client=self.http_client,
            id=id,
            params=params,
        )

    def update_resource_source_schema_by_examples(
        self, *, id: str, params: UpdateResourceSourceSchemaByExamplesParams
    ) -> ResourceSource:
        """update_resource_source_schema_by_examples updates a resource source schema by providing example data payloads.

        Instead of manually defining the JSON schema structure, you send representative examples of the data
        your resource source returns, and the system automatically infers the schema from these examples.

        Note: requires a `Management` API key."""
        return update_resource_source_schema_by_examples(
            client=self.http_client,
            id=id,
            params=params,
        )

    def delete_resource_source(self, *, id: str) -> None:
        """delete_resource_source permanently deletes a resource source. This action cannot be undone.

        Note: requires a `Management` API key."""
        delete_resource_source(
            client=self.http_client,
            id=id,
        )

    # ==================== Traffic Group Operations ====================

    def create_traffic_group(self, *, params: CreateTrafficGroupParams) -> TrafficGroup:
        """create_traffic_group creates a new traffic group.

        Note: requires a `Management` API key."""
        return create_traffic_group(
            client=self.http_client,
            params=params,
        )

    def list_traffic_groups(self) -> TrafficGroupsList:
        """list_traffic_groups retrieves all traffic groups.

        Note: requires a `Management` API key."""
        return list_traffic_groups(client=self.http_client)

    def update_traffic_group(
        self, *, traffic_group_id: str, params: UpdateTrafficGroupParams
    ) -> TrafficGroup:
        """update_traffic_group updates an existing traffic group.

        Note: requires a `Management` API key."""
        return update_traffic_group(
            client=self.http_client,
            traffic_group_id=traffic_group_id,
            params=params,
        )

    def delete_traffic_group(self, *, traffic_group_id: str) -> None:
        """delete_traffic_group deletes a traffic group and all associated targets.

        Note: requires a `Management` API key."""
        delete_traffic_group(
            client=self.http_client,
            traffic_group_id=traffic_group_id,
        )

    def create_traffic_group_target(
        self,
        *,
        traffic_group_id: str,
        params: CreateTrafficGroupTargetParams,
    ) -> TrafficGroupTarget:
        """create_traffic_group_target adds a target to a traffic group.

        Note: requires a `Management` API key."""
        return create_traffic_group_target(
            client=self.http_client,
            traffic_group_id=traffic_group_id,
            params=params,
        )

    def delete_traffic_group_target(
        self, *, traffic_group_id: str, target_id: str
    ) -> None:
        """delete_traffic_group_target removes a target from a traffic group.

        Note: requires a `Management` API key."""
        delete_traffic_group_target(
            client=self.http_client,
            traffic_group_id=traffic_group_id,
            target_id=target_id,
        )

    # ==================== Voice Call Context ====================

    def read_voice_call_context(
        self,
        *,
        phone_number: str,
        params: Optional[VoiceCallContextReadParams] = None,
    ) -> VoiceCallContext:
        """read_voice_call_context returns the most recent voice call context for a
        given phone number, for use in data-dip integrations with contact-centre platforms."""
        return read_voice_call_context(
            client=self.http_client,
            phone_number=phone_number,
            params=params,
        )

    # ==================== Back-Office Task Operations ====================

    def create_back_office_task(
        self, *, params: BackOfficeTaskCreateParams
    ) -> BackOfficeTask:
        """create_back_office_task creates a new back-office task.

        params.agent_id is the agent (agent group, prefix `agent_`) that runs the
        task, and params.procedure_id is the procedure (prefix `proc_`) within that
        agent to start the task from."""
        return create_back_office_task(
            client=self.http_client,
            params=params,
        )

    def read_back_office_task(self, *, task_id: str) -> BackOfficeTask:
        """read_back_office_task retrieves a back-office task by its external ID."""
        return read_back_office_task(
            client=self.http_client,
            task_id=task_id,
        )

    # ==================== Terminology Substitution Operations ====================

    def create_terminology_substitution(
        self, *, params: TerminologySubstitutionCreateParams
    ) -> TerminologySubstitution:
        """create_terminology_substitution creates a new terminology substitution.

        Note: requires a `Management` API key."""
        return create_terminology_substitution(
            client=self.http_client,
            params=params,
        )

    def list_terminology_substitutions(self) -> List[TerminologySubstitution]:
        """list_terminology_substitutions returns all terminology substitutions.

        Note: requires a `Management` API key."""
        return list_terminology_substitutions(client=self.http_client)

    def read_terminology_substitution(
        self, *, substitution_id: str
    ) -> TerminologySubstitution:
        """read_terminology_substitution retrieves a terminology substitution by ID.

        Note: requires a `Management` API key."""
        return read_terminology_substitution(
            client=self.http_client,
            substitution_id=substitution_id,
        )

    def update_terminology_substitution(
        self, *, substitution_id: str, params: TerminologySubstitutionUpdateParams
    ) -> TerminologySubstitution:
        """update_terminology_substitution updates an existing terminology substitution.

        Note: requires a `Management` API key."""
        return update_terminology_substitution(
            client=self.http_client,
            substitution_id=substitution_id,
            params=params,
        )

    def delete_terminology_substitution(self, *, substitution_id: str) -> None:
        """delete_terminology_substitution permanently deletes a terminology substitution.

        Note: requires a `Management` API key."""
        delete_terminology_substitution(
            client=self.http_client,
            substitution_id=substitution_id,
        )

    # ==================== Traffic Group Exclusions ====================

    def create_traffic_group_exclusion(
        self,
        *,
        group_id: str,
        params: TrafficGroupExclusionCreateParams,
    ) -> TrafficGroupTarget:
        """create_traffic_group_exclusion prevents a procedure from being selected for
        conversations in a traffic group, even when the procedure is unassigned/global.

        Note: requires a `Management` API key."""
        return create_traffic_group_exclusion(
            client=self.http_client,
            group_id=group_id,
            params=params,
        )

    def delete_traffic_group_exclusion(self, *, group_id: str, target_id: str) -> None:
        """delete_traffic_group_exclusion removes an exclusion from a traffic group.

        Note: requires a `Management` API key."""
        delete_traffic_group_exclusion(
            client=self.http_client,
            group_id=group_id,
            target_id=target_id,
        )

    # ==================== IP Addresses ====================

    def list_ip_addresses(self) -> IPAddresses:
        """list_ip_addresses returns the CIDR ranges used by the API and the egress IP.

        Useful for customers who need to whitelist Gradient Labs IPs in their firewall
        or security-group rules."""
        return list_ip_addresses(client=self.http_client)
