from web3.auto import w3
from eth_keys import keys
from eth_account.messages import encode_defunct
from eth_keys.datatypes import PrivateKey
from pydantic import BaseModel, parse_obj_as

from .SessionClient import SessionClient
from .exceptions import DexilonAuthException, DexilonEventException

URL = 'https://dex-dev-api.cronrate.com/api/v1'

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class DexilonClientBase:

    def __init__(self, metamask_address: str, api_secret: str) -> None:
        """ Dexilon API Client constructor

        :param metamask_address: Public Metamask Address
        :type metamask_address: str.
        :param api_secret: Api Secret
        :type api_secret: str.
        """

        self.metamask_address: str = metamask_address
        self.private_key: PrivateKey = keys.PrivateKey(
            bytes.fromhex(api_secret)
        )
        self.client: SessionClient = SessionClient(URL, HEADERS)

    def _handle_event(self, event_type: str, event_data: dict):
        if event_type == 'REJECTED':
            raise DexilonEventException(event_data['cause'])

    def _handle_response(self, response: dict, model: BaseModel = None) -> BaseModel:
        data: dict = response['body']
        if 'eventType' in data or 'event' in data:
            self._handle_event(
                event_type=data.get('eventType'),
                event_data=data.get('event')
            )
        elif model:
            return parse_obj_as(model, data)
        else:
            return data

    def _request(self, method: str, path: str, params: dict = None, data: dict = None, model: BaseModel = None) -> BaseModel:

        return self._handle_response(
            response=self.client.request(
                method=method,
                path=path,
                params=params,
                data=data
            ),
            model=model
        )

    def authenticate(self):

        nonce_response = self.client.request('POST', '/auth/startAuth', data={
            'metamaskAddress': self.metamask_address
        })

        nonce = nonce_response['body']['nonce']

        if not nonce:
            raise DexilonAuthException(
                'nonce was not received for Authentication request'
            )

        signature: bytes = w3.eth.account.sign_message(
            encode_defunct(str.encode(nonce)), private_key=self.private_key
        ).signature

        auth_info = self.client.request('POST', '/auth/finishAuth', data={
            'metamaskAddress': self.metamask_address,
            'signedNonce': signature.hex()
        })

        jwt_token = auth_info['body']['jwt']

        if not jwt_token:
            raise DexilonAuthException(
                'Was not able to obtain JWT token for authentication'
            )

        self.client.update_headers({
            'Authorization': 'Bearer {}'.format(jwt_token),
            'MetamaskAddress': self.metamask_address
        })
