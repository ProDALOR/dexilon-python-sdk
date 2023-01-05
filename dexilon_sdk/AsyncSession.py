import asyncio

from .BaseSession import BaseSession

import httpx
from pydantic import BaseModel


class AsyncSession(BaseSession):

    def __init__(self, base_url: str, timeout: float, headers: dict = {}) -> None:

        self.client: httpx.AsyncClient = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout
        )

    def update_headers(self, headers: dict = ...) -> None:
        self.client.headers.update(headers)

    def delete_header(self, header_name: str) -> None:
        self.client.headers.pop(header_name)

    async def async_request(self, method: str, path: str, model: BaseModel, params: dict = None, data: dict = None):
        response = await self.client.request(
            method=method,
            url=path,
            params=params,
            json=data
        )

        return self.check_response(response.status_code, response.text, model)

    def request(self, method: str, path: str, params: dict = None, data: dict = None, model: BaseModel = None):
        return asyncio.create_task(
            self.async_request(method, path, model, params, data)
        )
