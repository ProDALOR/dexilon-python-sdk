from typing import Union, Awaitable

from .BaseSession import BaseSession

from .chain_responses import CosmosAddressMapping, DexilonAccountInfo, CosmosFaucetResponse, \
    DexilonRegistrationTransactionInfo


class ChainMethods:

    chain: BaseSession

    def _get_cosmos_address_mapping(self, eth_address: str) -> Union[CosmosAddressMapping, Awaitable[CosmosAddressMapping]]:
        return self.chain.request('GET', f'/dexilon-exchange/dexilonl2/registration/address_mapping/mirror/{eth_address}', model=CosmosAddressMapping)

    def _get_cosmos_account_info(self, cosmos_address: str) -> Union[DexilonAccountInfo, Awaitable[DexilonAccountInfo]]:
        return self.chain.request('GET', f'/cosmos/auth/v1beta1/accounts/{cosmos_address}', model=DexilonAccountInfo)

    def _call_cosmos_faucet(self, cosmos_address: str) -> Union[CosmosFaucetResponse, Awaitable[CosmosFaucetResponse]]:
        return self.chain.request('POST', '/faucet', model=CosmosFaucetResponse, data={
            'address': cosmos_address
        })

    def _register_new_user_in_chain(self, data: dict) -> Union[DexilonRegistrationTransactionInfo, Awaitable[DexilonRegistrationTransactionInfo]]:
        return self.chain.request('POST', '/cosmos/tx/v1beta1/txs', model=DexilonRegistrationTransactionInfo, data=data)
