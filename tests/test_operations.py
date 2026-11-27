import re
from pathlib import Path

import pytest

from gradient_labs import Client

# OPERATIONS maps each public API contract operation id the library implements to
# the Client method that calls it. Update it with PUBLIC_API_VERSION when the
# library catches up with a new version of the contract.
#
# GET /spec.json (operation id `Spec`) is deliberately not exposed.
OPERATIONS = {
    "ArticleUpsert": "upsert_article",
    "ArticleSetUsageStatus": "set_article_usage_status",
    "ArticleDelete": "delete_article",
    "BackOfficeTaskCreate": "create_back_office_task",
    "BackOfficeTaskDelete": "delete_back_office_task",
    "BackOfficeTaskRead": "read_back_office_task",
    "ConversationStart": "start_conversation",
    "ConversationCancel": "cancel_conversation",
    "ConversationFinish": "finish_conversation",
    "ConversationAddMessage": "add_message",
    "ConversationResume": "resume_conversation",
    "ConversationReturnAsyncToolResult": "return_async_tool_result",
    "ConversationDelete": "delete_conversation",
    "ConversationReadDeprecated": "read_conversation_deprecated",
    "ConversationAssign": "assign_conversation",
    "ConversationEvent": "add_conversation_event",
    "ConversationRate": "rate_conversation",
    "ConversationRead": "read_conversation",
    "CustomerMemoriesList": "list_customer_memories",
    "CustomerMemoriesBatchCreate": "batch_create_customer_memories",
    "CustomerMemoriesBatchCreateV2": "batch_create_customer_memories_v2",
    "FileUploadBegin": "begin_file_upload",
    "FileList": "list_files",
    "FileCreate": "create_file",
    "HandOffTargetDelete": "delete_hand_off_target",
    "ListHandOffTargets": "list_handoff_targets",
    "HandOffTargetUpsert": "upsert_hand_off_target",
    "GetDefaultHandOffTarget": "get_default_hand_off_target",
    "SetDefaultHandOffTarget": "set_default_hand_off_target",
    "IPAddressList": "list_ip_addresses",
    "KnowledgeBaseList": "list_knowledge_bases",
    "KnowledgeBaseCreate": "create_knowledge_base",
    "KnowledgeBaseRead": "read_knowledge_base",
    "KnowledgeBaseUpdate": "update_knowledge_base",
    "NoteList": "list_notes",
    "NoteCreate": "create_note",
    "NoteDelete": "delete_note",
    "NoteRead": "read_note",
    "NoteUpdate": "update_note",
    "NoteSetStatus": "set_note_status",
    "OutboundChatConversationStart": "start_outbound_chat_conversation",
    "OutboundEmailConversationStart": "start_outbound_email_conversation",
    "OutboundPhoneConversationStart": "start_outbound_phone_conversation",
    "ReadProcedure": "read_procedure",
    "SetProcedureLimit": "set_procedure_limit",
    "ListProcedures": "list_procedures",
    "ProcedureListVersions": "list_procedure_versions",
    "ProcedureSetGatedVersion": "set_procedure_gated_version",
    "ProcedureSetLiveVersion": "set_procedure_live_version",
    "ProcedureUnsetGatedVersion": "unset_procedure_gated_version",
    "ProcedureUnsetLiveVersion": "unset_procedure_live_version",
    "ResourceSourceList": "list_resource_sources",
    "ResourceSourceCreate": "create_resource_source",
    "ResourceSourceDelete": "delete_resource_source",
    "ResourceSourceRead": "read_resource_source",
    "ResourceSourceUpdate": "update_resource_source",
    "UpdateSchemaByExamples": "update_resource_source_schema_by_examples",
    "ResourceTypeList": "list_resource_types",
    "ResourceTypeCreate": "create_resource_type",
    "ResourceTypeDelete": "delete_resource_type",
    "ResourceTypeRead": "read_resource_type",
    "ResourceTypeUpdate": "update_resource_type",
    "SecretList": "list_secrets",
    "SecretRevoke": "revoke_secret",
    "SecretWrite": "write_secret",
    "TerminologySubstitutionList": "list_terminology_substitutions",
    "TerminologySubstitutionCreate": "create_terminology_substitution",
    "TerminologySubstitutionDelete": "delete_terminology_substitution",
    "TerminologySubstitutionRead": "read_terminology_substitution",
    "TerminologySubstitutionUpdate": "update_terminology_substitution",
    "ToolList": "list_tools",
    "ToolCreate": "create_tool",
    "ToolDelete": "delete_tool",
    "ToolRead": "read_tool",
    "ToolUpdate": "update_tool",
    "ToolExecute": "execute_tool",
    "ReadTopic": "read_topic",
    "ListTopics": "list_topics",
    "ArticleTopicUpsert": "upsert_article_topic",
    "ListTrafficGroups": "list_traffic_groups",
    "TrafficGroupCreate": "create_traffic_group",
    "TrafficGroupDelete": "delete_traffic_group",
    "TrafficGroupUpdate": "update_traffic_group",
    "TrafficGroupExclusionCreate": "create_traffic_group_exclusion",
    "TrafficGroupExclusionDelete": "delete_traffic_group_exclusion",
    "TrafficGroupTargetCreate": "create_traffic_group_target",
    "TrafficGroupTargetDelete": "delete_traffic_group_target",
    "VoiceCallContextRead": "read_voice_call_context",
}


@pytest.mark.parametrize("operation_id,method", sorted(OPERATIONS.items()))
def test_operation_has_method(operation_id, method):
    assert callable(getattr(Client, method, None)), (
        f"{operation_id} should be implemented by Client.{method}"
    )


def test_spec_is_not_exposed():
    assert "Spec" not in OPERATIONS
    assert not hasattr(Client, "read_spec")


def test_public_api_version_is_a_contract_hash():
    version = Path(__file__).resolve().parent.parent / "PUBLIC_API_VERSION"
    assert re.fullmatch(r"[0-9a-f]{64}\n", version.read_text())
