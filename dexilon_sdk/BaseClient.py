from typing import Dict, List, Optional, Callable
import json

from pydantic import BaseModel, parse_obj_as, ValidationError

from .BaseSession import BaseSession
from .ApiMethods import ApiMethods
from .ChainMethods import ChainMethods
from .KeyChain import KeyChain
from .AbiLoader import AbiLoader

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

    TIME_BETWEEN_BLOCKS: int = 5
    BRIDGE_CONTRACT_ADDRESS: str = '0x1f4878d95d26C050D854D187De9d8FD4A8A3eE47'
    TOKEN_ADDRESS: str = "0x8f54629e7d660871abab8a6b4809a839ded396de"

    DECIMALS_USDC: int = 6

    NUMBER_OF_RETRIES_WAITING_FOR_FUNDS_AT_CONTRACT: int = 10
    DELAY_BETWEEN_RETRIES_WAITING_FOR_FUNDS_AT_CONTRACT: int = 10

    RPC_LIST: List[str] = [
        "https://polygon-mumbai.g.alchemy.com/v2/fjT6Ftkwr6805C0Guo_eicthIqtL1Yev",
        "https://rpc-mumbai.matic.today",
        "https://matic-mainnet.chainstacklabs.com",
        "https://rpc-mumbai.maticvigil.com"
    ]

    HEADERS: Dict[str, str] = {
        'Accept': 'application/json'
    }
    COSMOS_HEADERS: Dict[str, str] = {
        'Accept': 'application/json'
    }

    TIMEOUT: float = 20

    api: BaseSession
    chain: BaseSession

    def __init__(self, private_key: Optional[str] = None, mnemonic: Optional[str] = None) -> None:

        self.keys = KeyChain(
            eth_chain_id=self.ETH_CHAIN_ID,
            dexilon_chain_id=self.DEXILON_CHAIN_ID,
            private_key=private_key,
            mnemonic=mnemonic
        )

        self.abi = AbiLoader()

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

    def get_final_eth_amount(self, amount: int) -> int:
        return int(
            int(1_000_000 * float(amount)) * 10
            ** self.DECIMALS_USDC / 1_000_000
        )

    def get_final_dexilon_amount(self, amount: int) -> str:
        return f'{amount}000000000000000000'

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
            try:
                return parse_obj_as(model, data)
            except ValidationError:
                raise DexilonRequestException(
                    message=f'Invalid model for api response: {text}'
                )

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
            try:
                return parse_obj_as(model, data)
            except ValidationError:
                raise DexilonRequestException(
                    message=f'Invalid model for chain response: {text}'
                )

        return data

    def _prepare_method(self, func: Callable) -> Callable:
        return func
