from ._http_client import HttpClient
from .customer_memory import CustomerMemoriesList


def list_customer_memories(
    *, client: HttpClient, customer_id: str
) -> CustomerMemoriesList:
    """list_customer_memories lists all memories retained for a customer.

    Note: requires an `Integration` API key."""
    rsp = client.get(path=f"customers/{customer_id}/memories")
    return CustomerMemoriesList.from_dict(rsp)
