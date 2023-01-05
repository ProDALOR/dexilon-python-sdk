from typing import List, Union, Awaitable

from .BaseSession import BaseSession

from .responses import SymbolStats, ServerTime, ExchangeInformation, JWTTokenResponse, \
    AllOpenOrders, AccountInfo, OrderBookInfo, LeverageEvent, OrderEvent


def auth(func):
    func.auth = True
    return func


class ApiMethods:

    api: BaseSession

    def _get_access_token(self, payload: dict) -> Union[JWTTokenResponse, Awaitable[JWTTokenResponse]]:
        return self.api.request('POST', '/auth/accessToken', data=payload, model=JWTTokenResponse)

    def _refresh_token(self, payload: dict) -> Union[JWTTokenResponse, Awaitable[JWTTokenResponse]]:
        return self.api.request('POST', '/auth/refreshToken', data=payload, model=JWTTokenResponse)

    def ping(self) -> Union[dict, Awaitable[dict]]:
        return self.api.request('GET', '/system/ping')

    def get_all_symbols(self) -> Union[List[SymbolStats], Awaitable[List[SymbolStats]]]:
        return self.api.request('GET', '/symbols', model=List[SymbolStats])

    def get_server_time(self) -> Union[ServerTime, Awaitable[ServerTime]]:
        return self.api.request('GET', '/system/time', model=ServerTime)

    def get_exchange_information(self) -> Union[ExchangeInformation, Awaitable[ExchangeInformation]]:
        return self.api.request('GET', '/system/exchangeInfo', model=ExchangeInformation)

    def get_orderbook(self, symbol: str) -> Union[OrderBookInfo, Awaitable[OrderBookInfo]]:
        return self.api.request('GET', '/orders/book', model=OrderBookInfo, params={
            'symbol': symbol
        })

    @auth
    def get_account_info(self) -> Union[AccountInfo, Awaitable[AccountInfo]]:
        return self.api.request('GET', '/accounts', model=AccountInfo)

    @auth
    def set_leverage(self, symbol: str, leverage: int) -> Union[LeverageEvent, Awaitable[LeverageEvent]]:
        return self.api.request('PUT', '/accounts/leverage', model=LeverageEvent, data={
            'symbol': symbol,
            'leverage': leverage
        })

    @auth
    def get_open_orders(self) -> Union[AllOpenOrders, Awaitable[AllOpenOrders]]:
        return self.api.request('GET', '/orders/open', model=AllOpenOrders)

    @auth
    def get_order_info(self, symbol: str, client_order_id: str = None, order_id: str = None) -> Union[OrderEvent, Awaitable[OrderEvent]]:
        return self.api.request('GET', '/orders', model=OrderEvent, params={
            'symbol': symbol,
            **({'orderId': order_id} if order_id else {}),
            **({'clientOrderId': client_order_id} if client_order_id else {})
        })

    @auth
    def limit_order(self, symbol: str, side: str, size: float, price: float, client_order_id: str = None) -> Union[OrderEvent, Awaitable[OrderEvent]]:
        return self.api.request('POST', '/orders/limit', model=OrderEvent, data={
            'symbol': symbol,
            'side': side,
            'size': size,
            'price': price,
            **({'clientOrderId': client_order_id} if client_order_id else {})
        })

    @auth
    def market_order(self, symbol: str, side: str, size: float, client_order_id: str = None) -> Union[OrderEvent, Awaitable[OrderEvent]]:
        return self.api.request('POST', '/orders/market', model=OrderEvent, data={
            'symbol': symbol,
            'side': side,
            'size': size,
            **({'clientOrderId': client_order_id} if client_order_id else {})
        })

    @auth
    def cancel_order(self, symbol: str, client_order_id: str = None, order_id: str = None) -> Union[OrderEvent, Awaitable[OrderEvent]]:
        return self.api.request('DELETE', '/orders', model=OrderEvent, data={
            'symbol': symbol,
            **({'orderId': order_id} if order_id else {}),
            **({'clientOrderId': client_order_id} if client_order_id else {})
        })

    @auth
    def cancel_all_orders(self) -> Union[List[OrderEvent], Awaitable[List[OrderEvent]]]:
        return self.api.request('DELETE', '/orders/all', model=List[OrderEvent])
