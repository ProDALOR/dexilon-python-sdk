from typing import List

from .DexilonClientBase import DexilonClientBase

from .responses import AvailableSymbol, OrderBookInfo, MarginData, OrderInfo, OrdersBySymbols


class DexilonClient(DexilonClientBase):

    def get_all_symbols(self) -> List[AvailableSymbol]:
        """
        Get all available symbols
        :return: AvailableSymbol[]
        """

        return self._request('GET', '/symbols', model=List[AvailableSymbol])

    def get_orderbook(self, symbol: str) -> OrderBookInfo:
        """
        Get latest orderbook by symbol
        :return: OrderBookInfo
        """

        return self._request('GET', '/orders/book', model=OrderBookInfo, params={
            'symbol': symbol
        })

    def get_margin(self) -> MarginData:
        """
        :return:
        MarginData
        """
        return self._request('GET', '/margin', model=MarginData)

    # TODO
    def get_order_info(self, order_id: str) -> OrderInfo:
        """
        Returns order information by orderId
        :param order_id: Dexilon order id
        :type order_id: str
        :return: OrderInfo
        """

        pass

    # TODO
    def get_open_orders(self):
        """
        Returns full list of open orders
        :return: OrdersBySymbol[]
        """

        return self._request('GET', '/orders/open')

    # TODO
    def limit_order(self, symbol: str, side: str, price: float, size: float, client_order_id: str):
        """
        Submit new limit order
        :param client_order_id: generated on client side order id
        :type client_order_id: str.
        :param symbol: order symbol
        :type symbol: str.
        :param side: order side [BUY, SELL]
        :type side: str.
        :param size: amount of the order asset
        :type size: float
        :param price: limit price
        :type price: float
        :return: Dexilon generated order id
        """

        return self._request('POST', '/orders/limit', data={
            'clientorderId': client_order_id,
            'symbol': symbol,
            'side': side,
            'size': size,
            'price': price
        })

    # TODO
    def market_order(self, symbol: str, side: str, size: float, client_order_id: str):
        """
        Submit new market order
        :param client_order_id: generated on client side order id
        :type client_order_id: str.
        :param symbol: order symbol
        :type symbol: str.
        :param side: order side [BUY, SELL]
        :type side: str.
        :param size: amount of the order asset
        :type size: float
        :return: Dexilon generated order id
        """

        return self._request('POST', '/orders/market', data={
            'clientorderId': client_order_id,
            'symbol': symbol,
            'side': side,
            'size': size
        })

    # TODO
    def cancel_all_orders(self):
        """
        Cancel all open orders
        :return: result bool
        """

        return self._request('DELETE', '/orders/batch')

    # TODO
    def cancel_order(self, order_id: str, symbol: str):
        """
        Cancel specific order by order id and symbol
        :param order_id: str
        :param symbol:
        :return: result bool
        """

        return self._request('DELETE', '/orders/batch', params={
            'symbol': symbol,
            'orderId': order_id
        })
