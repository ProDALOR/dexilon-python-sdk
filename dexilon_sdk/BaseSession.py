from typing import Union

from pydantic import BaseModel


class BaseSession:

    def __init__(self, base_url: str, timeout: float, headers: dict = {}) -> None:
        raise NotImplementedError()

    def check_response(self, status_code: int, text: str, model: BaseModel = None) -> Union[BaseModel, dict, None]:
        raise NotImplementedError()

    def request(self, method: str, path: str, params: dict = None, data: dict = None, model: BaseModel = None) -> BaseModel:
        raise NotImplementedError()

    def update_headers(self, headers: dict = {}) -> None:
        raise NotImplementedError()

    def delete_header(self, header_name: str) -> None:
        raise NotImplementedError()
