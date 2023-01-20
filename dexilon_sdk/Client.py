from typing import Callable, Optional

from web3 import Web3

from .BaseClient import BaseClient
from .SyncSession import SyncSession

from .exceptions import DexilonApiAuthException, DexilonChainAuthException, \
    DexilonRequestException
from .cosmospy import Transaction


class Client(BaseClient):

    def __init__(self, private_key: Optional[str] = None, mnemonic: Optional[str] = None) -> None:

        self.api = SyncSession(
            base_url=self.DEXILON_API_URL,
            headers=self.HEADERS,
            timeout=self.TIMEOUT
        )

        self.chain = SyncSession(
            base_url=self.DEXILON_CHAIN_URL,
            headers=self.COSMOS_HEADERS,
            timeout=self.TIMEOUT
        )

        super().__init__(private_key, mnemonic)

    def _rpc_connect(self) -> Web3:
        for rpc in self.RPC_LIST:
            w3 = Web3(Web3.HTTPProvider(rpc))
            if w3.isConnected():
                return w3

    def _generate_new_cosmos_address(self) -> str:

        cosmos_wallet = self.keys.generate_cosmos_wallet()

        cosmos_address = cosmos_wallet.address
        eth_address = self.keys.address

        self._call_cosmos_faucet(cosmos_address)

        account_info = self._get_cosmos_account_info(cosmos_address)

        cosmos_account_number = account_info.account.account_number
        cosmos_account_sequence = account_info.account.sequence
        signature = self.keys.sign(cosmos_address)

        cosmo_tx = Transaction(
            privkey=cosmos_wallet.private_key,
            account_num=cosmos_account_number,
            sequence=cosmos_account_sequence,
            fee=0,
            fee_denom="dxln",
            gas=200_000,
            memo="",
            chain_id=self.DEXILON_CHAIN_ID,
        )

        cosmo_tx.add_registration(
            creator=cosmos_address,
            chainId=self.ETH_CHAIN_ID,
            address=eth_address,
            signature=signature,
            signedMessage=cosmos_address
        )

        cosmos_faucet_response = self._register_new_user_in_chain({
            'tx_bytes': cosmo_tx.get_tx_bytes(),
            'mode': 'BROADCAST_MODE_BLOCK'
        })

        if cosmos_faucet_response.tx_response.code != 0:
            raise DexilonRequestException(
                f'Error trying to register new user [{cosmos_address}] in Dexilon network'
            )

        return cosmos_address

    def prolongate(self) -> None:

        auth_info = self._refresh_token(self.keys.payload_to_refresh_token())
        self.keys.set_tokens(auth_info.accessToken, auth_info.refreshToken)
        self.api.update_headers(self.keys.auth_headers)

    def authenticate(self) -> None:

        try:

            dexilon_address = self._get_cosmos_address_mapping(
                self.keys.address
            )
            cosmos_address = dexilon_address.addressMapping.cosmosAddress

        except DexilonChainAuthException:

            cosmos_address = self._generate_new_cosmos_address()

        self.keys.set_cosmos_address(cosmos_address)

        auth_info = self._get_access_token(
            self.keys.payload_to_get_access_token()
        )

        self.keys.set_tokens(auth_info.accessToken, auth_info.refreshToken)
        self.api.update_headers(self.keys.auth_headers)

    def _prepare_method(self, func: Callable) -> Callable:
        def method(*args, **kwargs):
            try:
                if getattr(func.__func__, 'auth', False) and not self.keys:
                    self.authenticate()
                return func(*args, **kwargs)
            except DexilonApiAuthException:
                self.authenticate()
                return func(*args, **kwargs)
        return method
