from .BaseSession import BaseSession

import httpx
from pydantic import BaseModel


class SyncSession(BaseSession):

    def __init__(self, base_url: str, timeout: float, headers: dict = {}) -> None:

        self.client: httpx.Client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout
        )

    def update_headers(self, headers: dict = ...) -> None:
        self.client.headers.update(headers)

    def delete_header(self, header_name: str) -> None:
        self.client.headers.pop(header_name)

    def request(self, method: str, path: str, params: dict = None, data: dict = None, model: BaseModel = None):

        response = self.client.request(
            method=method,
            url=path,
            params=params,
            json=data
        )

        return self.check_response(response.status_code, response.text, model)
