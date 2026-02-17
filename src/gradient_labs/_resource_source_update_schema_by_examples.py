from typing import List, Any, Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from ._http_client import HttpClient
from .resource_source import ResourceSource, SchemaUpdateStrategy


@dataclass_json
@dataclass(frozen=True)
class UpdateResourceSourceSchemaByExamplesParams:
    """UpdateResourceSourceSchemaByExamplesParams contains the parameters for updating a resource source schema by examples."""

    # Examples is an array of example data payloads that represent the structure
    # of the data your resource source returns.
    examples: List[Any]

    # SchemaUpdateStrategy controls how the new schema is applied.
    # Defaults to "merge" if not specified.
    schema_update_strategy: Optional[SchemaUpdateStrategy] = None


def update_resource_source_schema_by_examples(
    *, client: HttpClient, id: str, params: UpdateResourceSourceSchemaByExamplesParams
) -> ResourceSource:
    """update_resource_source_schema_by_examples updates a resource source schema by providing example data payloads.

    Instead of manually defining the JSON schema structure, you send representative examples of the data
    your resource source returns, and the system automatically infers the schema from these examples.

    Note: requires a Management API key.
    """
    body = {
        "examples": params.examples,
    }
    if params.schema_update_strategy is not None:
        body["schema_update_strategy"] = params.schema_update_strategy.value

    rsp = client.post(path=f"resource-sources/{id}/schema-by-examples", body=body)
    return ResourceSource.from_dict(rsp)
