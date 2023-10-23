import time

import requests

from cex_arb.utils.average_price_calculator import AveragePriceCalculator


class BrasilBitcoin:
    def __init__(self):
        self.BRASIL_BITCOIN_API_BASE_URL = "http://brasilbitcoin.com.br/API"
        self.ORDER_BOOK_URL = self.BRASIL_BITCOIN_API_BASE_URL + "/orderbook"
        self.price_calculator = AveragePriceCalculator()

    @staticmethod
    def _get_headers():
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                          'Safari/537.36 ',
            'Authentication': 'yKIS2zlsHTqGe0FwxwJiJqIBFEhE6NhO'
        }
        return headers

    def _get_order_book(self, symbol):
        ORDER_BOOK_URL = self.ORDER_BOOK_URL + "/%s" % symbol
        ask_bid = requests.post(url=ORDER_BOOK_URL, headers=self._get_headers()).json()
        asks = ask_bid['sell']
        bids = ask_bid['buy']
        return asks, bids

    def get_average_token_price(self, symbol, BRL_to_trade, book_side):
        time.sleep(0.1)
        symbol = symbol.split('BRL')[0]
        token_amount = self._BRL_to_token(symbol, BRL_to_trade)
        asks, bids = self._get_order_book(symbol)
        if book_side == "asks":
            asks_manipulated = self.manipulate_order_book(asks)
            try:
                return self.price_calculator.calculate_average_price(asks_manipulated, token_amount)
            except:
                return -1
        if book_side == "bids":
            bids_manipulated = self.manipulate_order_book(bids)
            try:
                return self.price_calculator.calculate_average_price(bids_manipulated, token_amount)
            except:
                return -1
    @staticmethod
    def _BRL_to_token(symbol, BRL_to_trade):
        URL_PRICES = "https://brasilbitcoin.com.br/API/prices/%s" % symbol
        last_symbol_BRL = float(requests.get(url=URL_PRICES).json()['last'])
        symbol_amount = BRL_to_trade / last_symbol_BRL
        return symbol_amount

    @staticmethod
    def manipulate_order_book(data):
        new_data = []
        for order in data:
            new_data.append([order['preco'], order['quantidade']])
        return new_data




