from typing import Dict, Optional, Callable
import json

from pydantic import BaseModel, parse_obj_as

from .BaseSession import BaseSession
from .ApiMethods import ApiMethods
from .ChainMethods import ChainMethods
from .KeyChain import KeyChain

from .exceptions import DexilonAPIException, DexilonApiAuthException, DexilonRequestException, \
    DexilonChainException, DexilonChainAuthException

API_METHODS = [
    method for method in dir(ApiMethods)
    if not method.startswith('_')
]


class BaseClient(ApiMethods, ChainMethods):

    DEXILON_API_URL: str = 'https://api.staging.dexilon.io/api/v1'
    DEXILON_CHAIN_URL: str = 'https://proxy.staging.dexilon.io'

    ETH_CHAIN_ID: int = 80001
    DEXILON_CHAIN_ID: str = 'dexilon-staging'

    HEADERS: Dict[str, str] = {
        'Accept': 'application/json'
    }
    COSMOS_HEADERS: Dict[str, str] = {
        'Accept': 'application/json'
    }

    TIMEOUT: float = 20

    api: BaseSession
    chain: BaseSession

    def __init__(self, private_key: Optional[str] = None) -> None:

        self.keys = KeyChain(
            eth_chain_id=self.ETH_CHAIN_ID,
            dexilon_chain_id=self.DEXILON_CHAIN_ID,
            private_key=private_key
        )

        self.api.update_headers(self.keys.base_address_headers)
        self.api.check_response = self._check_api_response
        self.chain.check_response = self._check_chain_response

        for __name in API_METHODS:
            try:
                func = super().__getattribute__(__name)
                self.__setattr__(__name, self._prepare_method(func))
            except AttributeError:
                pass

    @property
    def address(self) -> str:
        return self.keys.address

    @property
    def dexilon_address(self) -> str:
        return self.keys.cosmos_address

    @property
    def private_key(self) -> str:
        return self.keys.private_key

    def _check_api_response(self, status_code: int, text: str, model: BaseModel) -> BaseModel:
        try:

            data: dict = json.loads(text)

        except ValueError:
            raise DexilonRequestException(
                message=f'Invalid api response: {text}'
            )

        if status_code == 401:
            raise DexilonApiAuthException.from_dict(data)

        if 'code' in data:
            raise DexilonAPIException.from_dict(data)

        if model:
            return parse_obj_as(model, data)

        return data

    def _check_chain_response(self, status_code: int, text: str, model: BaseModel) -> BaseModel:
        try:

            data: dict = json.loads(text)

        except ValueError:
            raise DexilonRequestException(
                message=f'Invalid chain response: {text}'
            )

        if status_code == 404:
            raise DexilonChainAuthException.from_dict(data)

        if 'code' in data:
            raise DexilonChainException.from_dict(data)

        if model:
            return parse_obj_as(model, data)

        return data

    def _prepare_method(self, func: Callable) -> Callable:
        return func
