import warnings
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from gradient_labs import (
    BatchCreateCustomerMemoriesDeprecatedParams,
    BatchCreateCustomerMemoriesParams,
    BatchCreateCustomerMemory,
    BatchCreateCustomerMemoryDeprecated,
    BeginFileUploadParams,
    Client,
    CreateFileParams,
    CreateKnowledgeBaseParams,
    CustomerMemoryType,
    FileListParams,
    NoteListParams,
    NoteStatus,
    UpdateKnowledgeBaseParams,
)

TIME = "2024-01-15T10:30:00Z"


def _client(method: str, response=None):
    client = Client(api_key="test-key")
    mock = MagicMock(return_value=response)
    setattr(client.http_client, method, mock)
    return client, mock


def _note(**extra):
    return {
        "gradient_labs_id": "note_01",
        "id": "spring-sale",
        "title": "Spring sale",
        "last_modified_by": "public-api",
        "status": "live",
        "created": TIME,
        "updated": TIME,
        **extra,
    }


def _knowledge_base():
    return {
        "gradient_labs_id": "knowledgebase_01",
        "id": "help-centre",
        "name": "Help Centre",
        "created": TIME,
        "updated": TIME,
    }


def _file():
    return {
        "id": "companyfile_01",
        "ref": "id-card-front",
        "file_name": "id-card-front.png",
        "content_type": "image/png",
        "size_bytes": 482113,
        "created": TIME,
    }


class TestNotes:
    def test_list_notes(self):
        client, get = _client(
            "get",
            {
                "notes": [_note(attributes={"Locale": ["UK"]})],
                "pagination": {"next": "cursor-2"},
            },
        )

        rsp = client.list_notes(params=NoteListParams(cursor="cursor-1"))

        _, kwargs = get.call_args
        assert kwargs["path"] == "notes"
        assert kwargs["query_params"] == {"cursor": "cursor-1"}
        assert rsp.notes[0].id == "spring-sale"
        assert rsp.notes[0].status == NoteStatus.LIVE
        assert rsp.notes[0].attributes == {"Locale": ["UK"]}
        assert rsp.pagination.next == "cursor-2"

    def test_list_notes_without_params(self):
        client, get = _client("get", {"notes": [], "pagination": {}})

        client.list_notes()

        assert get.call_args.kwargs["query_params"] == {}

    def test_read_note(self):
        client, get = _client("get", _note(body="20% off"))

        note = client.read_note(note_id="spring-sale")

        assert get.call_args.kwargs["path"] == "notes/spring-sale"
        assert note.body == "20% off"
        assert note.created.year == 2024


class TestKnowledgeBases:
    def test_list(self):
        client, get = _client("get", {"knowledge_bases": [_knowledge_base()]})

        rsp = client.list_knowledge_bases()

        assert get.call_args.kwargs["path"] == "knowledge-bases"
        assert rsp.knowledge_bases[0].id == "help-centre"

    def test_create(self):
        client, post = _client("post", _knowledge_base())

        kb = client.create_knowledge_base(
            params=CreateKnowledgeBaseParams(id="help-centre", name="Help Centre")
        )

        _, kwargs = post.call_args
        assert kwargs["path"] == "knowledge-bases"
        assert kwargs["body"] == {"id": "help-centre", "name": "Help Centre"}
        assert kb.gradient_labs_id == "knowledgebase_01"

    def test_read(self):
        client, get = _client("get", _knowledge_base())

        client.read_knowledge_base(knowledge_base_id="help-centre")

        assert get.call_args.kwargs["path"] == "knowledge-bases/help-centre"

    def test_update(self):
        client, post = _client("post", _knowledge_base())

        client.update_knowledge_base(
            knowledge_base_id="help-centre",
            params=UpdateKnowledgeBaseParams(name="Help"),
        )

        _, kwargs = post.call_args
        assert kwargs["path"] == "knowledge-bases/help-centre"
        assert kwargs["body"] == {"name": "Help"}


class TestFiles:
    def test_begin_upload(self):
        client, post = _client(
            "post",
            {
                "upload_id": "upload_1",
                "upload_url": "https://storage.example.com/upload_1",
                "content_type": "image/png",
                "headers": {"Content-Type": "image/png"},
                "expires_at": TIME,
                "max_bytes": 5242880,
            },
        )

        upload = client.begin_file_upload(
            params=BeginFileUploadParams(content_type="image/png")
        )

        _, kwargs = post.call_args
        assert kwargs["path"] == "file-uploads"
        assert kwargs["body"] == {"content_type": "image/png"}
        assert upload.upload_id == "upload_1"
        assert upload.headers == {"Content-Type": "image/png"}
        assert upload.max_bytes == 5242880

    def test_begin_upload_without_params(self):
        client, post = _client(
            "post",
            {
                "upload_id": "u",
                "upload_url": "https://storage.example.com/u",
                "content_type": "application/octet-stream",
                "headers": {},
                "expires_at": TIME,
                "max_bytes": 1,
            },
        )

        client.begin_file_upload()

        assert post.call_args.kwargs["body"] == {}

    def test_list(self):
        client, get = _client(
            "get", {"files": [_file()], "pagination": {"next": "cursor-2"}}
        )

        rsp = client.list_files(params=FileListParams(cursor="cursor-1"))

        _, kwargs = get.call_args
        assert kwargs["path"] == "files"
        assert kwargs["query_params"] == {"cursor": "cursor-1"}
        assert rsp.files[0].ref == "id-card-front"
        assert rsp.pagination.next == "cursor-2"

    def test_create(self):
        client, post = _client("post", _file())

        file = client.create_file(
            params=CreateFileParams(upload_id="upload_1", file_name="id.png")
        )

        _, kwargs = post.call_args
        assert kwargs["path"] == "files"
        assert kwargs["body"] == {"upload_id": "upload_1", "file_name": "id.png"}
        assert file.size_bytes == 482113


class TestCustomerMemories:
    def test_list(self):
        client, get = _client(
            "get",
            {
                "memories": [
                    {
                        "external_id": "order_123",
                        "custom_type": {
                            "name": "order_event",
                            "description": "An order",
                        },
                        "created_at": TIME,
                        "data": {"total": 10},
                    }
                ]
            },
        )

        rsp = client.list_customer_memories(customer_id="cust-1")

        assert get.call_args.kwargs["path"] == "customers/cust-1/memories"
        memory = rsp.memories[0]
        assert memory.custom_type.name == "order_event"
        assert memory.data == {"total": 10}

    def test_batch_create_v2(self):
        client, post = _client("post")

        client.batch_create_customer_memories_v2(
            customer_id="cust-1",
            params=BatchCreateCustomerMemoriesParams(
                memories=[
                    BatchCreateCustomerMemory(
                        external_id="order_123",
                        custom_type=CustomerMemoryType(name="order_event"),
                        created_at=datetime(2024, 1, 15, 10, 30),
                        data={"total": 10},
                    )
                ]
            ),
        )

        _, kwargs = post.call_args
        assert kwargs["path"] == "customers/cust-1/memories/v2"
        assert kwargs["body"] == {
            "memories": [
                {
                    "external_id": "order_123",
                    "custom_type": {"name": "order_event"},
                    "created_at": "2024-01-15T10:30:00.000000Z",
                    "data": {"total": 10},
                }
            ]
        }

    def test_batch_create_is_deprecated(self):
        client, post = _client("post")

        with pytest.warns(DeprecationWarning):
            client.batch_create_customer_memories(
                customer_id="cust-1",
                params=BatchCreateCustomerMemoriesDeprecatedParams(
                    memories=[
                        BatchCreateCustomerMemoryDeprecated(
                            external_id="order_123",
                            custom_type="order_event",
                            created_at=datetime(2024, 1, 15, 10, 30),
                            data={},
                        )
                    ]
                ),
            )

        _, kwargs = post.call_args
        assert kwargs["path"] == "customers/cust-1/memories"
        assert kwargs["body"]["memories"][0]["custom_type"] == "order_event"


class TestReadConversationDeprecated:
    def test_reads_the_deprecated_path(self):
        client, get = _client(
            "get",
            {
                "id": "conv-1",
                "customer_id": "cust-1",
                "channel": "web",
                "status": "active",
                "created": "2024-01-15T10:30:00+00:00",
                "updated": "2024-01-15T10:30:00+00:00",
            },
        )

        with pytest.warns(DeprecationWarning):
            conversation = client.read_conversation_deprecated(conversation_id="conv-1")

        assert get.call_args.kwargs["path"] == "conversations/conv-1"
        assert conversation.id == "conv-1"

    def test_read_conversation_does_not_warn(self):
        client, get = _client(
            "get",
            {
                "id": "conv-1",
                "customer_id": "cust-1",
                "channel": "web",
                "status": "active",
                "created": "2024-01-15T10:30:00+00:00",
                "updated": "2024-01-15T10:30:00+00:00",
            },
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            client.read_conversation(conversation_id="conv-1")

        assert get.call_args.kwargs["path"] == "conversations/conv-1/read"


def test_update_tool_preserves_unset_fields():
    from gradient_labs import ToolUpdateParams

    client, put = _client("put", {"id": "tool-1", "name": "search", "description": ""})
    client.update_tool(
        params=ToolUpdateParams(id="tool-1", description="Find an order")
    )
    put.assert_called_once_with(
        path="tools/tool-1", body={"description": "Find an order"}
    )


def test_tool_execute_with_public_argument():
    from gradient_labs import Argument, ToolExecuteParams

    client, post = _client("post", {"id": "run-1", "result": ["found"]})
    response = client.execute_tool(
        params=ToolExecuteParams(id="tool-1", arguments=[Argument("query", "books")])
    )
    post.assert_called_once_with(
        path="tools/tool-1/execute",
        body={"arguments": [{"name": "query", "value": "books"}]},
    )
    assert response.result == ["found"]


def test_article_topic_public_url_and_arbitrary_data():
    from gradient_labs import ArticleTopicUpsertParams, PublicationStatus, Visibility

    client, post = _client("post")
    client.upsert_article_topic(
        params=ArticleTopicUpsertParams(
            id="topic",
            name="Help",
            visibility=Visibility.PUBLIC,
            status=PublicationStatus.PUBLISHED,
            created=datetime(2024, 1, 1),
            last_edited=datetime(2024, 1, 2),
            data=[None, False],
            public_url="https://example.org/help",
        )
    )
    assert post.call_args.kwargs["body"]["public_url"] == "https://example.org/help"
    assert post.call_args.kwargs["body"]["data"] == [None, False]


def test_attachment_only_message_and_positional_replay():
    from gradient_labs import (
        AddMessageParams,
        Attachment,
        AttachmentType,
        ParticipantType,
    )

    client, post = _client(
        "post",
        {
            "id": "message",
            "body": "",
            "participant_type": "AI Agent",
            "participant_id": "agent",
        },
    )
    attachment = Attachment(
        AttachmentType.FILE, "receipt.pdf", url="https://example.org/receipt.pdf"
    )
    response = client.add_message(
        conversation_id="conv",
        params=AddMessageParams(
            id="message",
            participant_type=ParticipantType.AI_AGENT,
            attachments=[attachment],
        ),
    )
    assert post.call_args.kwargs["body"] == {
        "id": "message",
        "participant_type": "AI Agent",
        "attachments": [
            {
                "type": "file",
                "file_name": "receipt.pdf",
                "url": "https://example.org/receipt.pdf",
            }
        ],
    }
    assert response.participant_id == "agent"
    client.add_message(
        conversation_id="conv",
        params=AddMessageParams("message", "Hello", "agent", ParticipantType.AI_AGENT),
    )
    assert post.call_args.kwargs["body"]["body"] == "Hello"


@pytest.mark.parametrize("fraction,microsecond", [("1", 100000), ("123456789", 123456)])
def test_rfc3339_fractional_seconds(fraction, microsecond):
    from gradient_labs import CustomerMemory

    memory = CustomerMemory.from_dict(
        {
            "external_id": "order",
            "custom_type": {"name": "order"},
            "created_at": f"2025-01-02T03:04:05.{fraction}Z",
            "data": {},
        }
    )
    assert memory.created_at.microsecond == microsecond
    assert memory.created_at.utcoffset().total_seconds() == 0
