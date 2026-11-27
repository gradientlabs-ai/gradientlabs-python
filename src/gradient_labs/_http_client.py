from typing import Any, Callable, Optional
from datetime import datetime
from importlib import metadata

from pytz import UTC
import requests

from .errors import ResponseError

API_BASE_URL = "https://api.gradient-labs.ai"

try:
    _version = metadata.version("gradient-labs")
except metadata.PackageNotFoundError:
    # Running from a source tree with no installed distribution metadata.
    _version = "unknown"

USER_AGENT = f"Gradient Labs Python/{_version}"


class HttpClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = API_BASE_URL,
        timeout: int = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    def post(self, path: str, body: Any = None, query_params: Optional[dict] = None):
        return self._api_call(requests.post, path, body, query_params)

    def put(self, path: str, body: Any = None, query_params: Optional[dict] = None):
        return self._api_call(requests.put, path, body, query_params)

    def get(self, path: str, body: Any = None, query_params: Optional[dict] = None):
        return self._api_call(requests.get, path, body, query_params)

    def delete(self, path: str, body: Any = None, query_params: Optional[dict] = None):
        return self._api_call(requests.delete, path, body, query_params)

    @classmethod
    def localize(cls, timestamp: datetime) -> str:
        # Naive datetimes are taken to already be UTC, as they always have been.
        if timestamp.tzinfo is None:
            return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return timestamp.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _api_call(
        self,
        request_func: Callable,
        path: str,
        body: Any,
        query_params: Optional[dict] = None,
    ):
        url = f"{self.base_url}/{path}"
        rsp = request_func(
            url,
            json=body,
            params=query_params,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": USER_AGENT,
            },
            timeout=self.timeout,
        )

        if rsp.status_code < 200 or rsp.status_code > 299:
            raise ResponseError(rsp)
        if len(rsp.content) != 0:
            return rsp.json()
