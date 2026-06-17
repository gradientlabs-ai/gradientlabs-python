from ._http_client import HttpClient
from .ip_addresses import IPAddresses


def list_ip_addresses(*, client: HttpClient) -> IPAddresses:
    rsp = client.get(path="ip-addresses", body={})
    return IPAddresses.from_dict(rsp)
