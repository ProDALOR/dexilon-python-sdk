from typing import Optional
import time
import secrets

from pydantic import BaseModel
from web3 import Web3
from web3.auto import w3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct

from .cosmospy import generate_wallet


class CosmosWallet(BaseModel):
    seed: str
    derivation_path: str
    private_key: bytes
    public_key: bytes
    address: str


class KeyChain:

    PRIVATE_KEY_LENGTH: int = 32

    def __init__(self,
                 eth_chain_id: int,
                 dexilon_chain_id: str,
                 private_key: Optional[str] = None,
                 ) -> None:

        if not private_key:
            account = self.__generate_random_account()
        else:
            account = self.__get_account_from_private_key(private_key)

        self.eth_chain_id: int = eth_chain_id
        self.dexilon_chain_id: str = dexilon_chain_id

        self.address: str = account.address
        self.__private_key = account._key_obj

        self.cosmos_address: str = None

        self.__access_token: str = None
        self.__refresh_token: str = None

    @property
    def private_key(self) -> str:
        return self.__private_key._raw_key.hex()

    def __generate_random_account(self) -> LocalAccount:
        return Account.from_key(secrets.token_hex(self.PRIVATE_KEY_LENGTH))

    def __get_account_from_private_key(self, private_key: str) -> LocalAccount:
        return Account.from_key(private_key)

    def __bool__(self) -> bool:
        return bool(self.cosmos_address and self.__access_token)

    def set_cosmos_address(self, cosmos_address: str) -> None:
        self.cosmos_address = cosmos_address

    def set_tokens(self, access_token: str, refresh_token: str) -> None:
        self.__access_token = access_token
        self.__refresh_token = refresh_token

    @property
    def base_address_headers(self) -> dict:
        return {
            'MetamaskAddress': self.address
        }

    @property
    def auth_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.__access_token}',
            'CosmosAddress': self.cosmos_address
        }

    def sign(self, msg: str) -> str:
        return w3.eth.account.sign_message(
            encode_defunct(
                Web3.solidityKeccak(['string'], [msg])
            ),
            private_key=self.__private_key
        ).signature.hex()

    def payload_to_get_access_token(self) -> dict:
        timestamp = int(time.time())
        nonce = f'{timestamp}#{self.cosmos_address}'
        return {
            'ethAddress': self.address,
            'nonce': nonce,
            'signedNonce': self.sign(nonce)
        }

    def payload_to_refresh_token(self) -> dict:
        return {
            'refreshToken': self.__refresh_token
        }

    def generate_cosmos_wallet(self) -> CosmosWallet:
        return CosmosWallet(**generate_wallet())
