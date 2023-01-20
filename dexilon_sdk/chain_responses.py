from typing import Optional, List

from pydantic import BaseModel


class ChainErrorBody(BaseModel):
    code: int
    message: Optional[str]
    details: Optional[List[str]]


class AddressCosmosMapping(BaseModel):
    chainId: int
    address: str
    cosmosAddress: str


class CosmosAddressMapping(BaseModel):
    addressMapping: Optional[AddressCosmosMapping]
    code: Optional[int]
    message: Optional[str]


class DexilonAccount(BaseModel):
    address: Optional[str]
    account_number: Optional[int]
    sequence: Optional[int]


class DexilonAccountInfo(BaseModel):
    account: Optional[DexilonAccount]


class CosmosFaucetResponse(BaseModel):
    result: Optional[dict]


class DexilonRegistrationInfoData(BaseModel):
    txhash: Optional[str]
    code: Optional[int]


class DexilonRegistrationTransactionInfo(BaseModel):
    tx_response: DexilonRegistrationInfoData
