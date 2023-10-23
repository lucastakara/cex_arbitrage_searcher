import json
import time

import requests as requests

from cex_arb.utils.average_price_calculator import AveragePriceCalculator


class Binance:
    def __init__(self):
        self.BINANCE_API_BASE_URL = "https://api3.binance.com"
        self.ORDER_BOOK_DEPTH_URL = self.BINANCE_API_BASE_URL + "/api/v3/depth"
        self.TICKER_PRICE_URL = self.BINANCE_API_BASE_URL + "/api/v3/ticker/price"
        self.headers = self._get_headers()
        self.price_calculator = AveragePriceCalculator()

    @staticmethod
    def _get_headers():
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                          'Safari/537.36 '
        }
        return headers

    @staticmethod
    def _get_params(symbol, limit):
        params = {
            "symbol": symbol,
            "limit": limit
        }
        return params

    def _get_order_book(self, symbol, limit=200):
        params = self._get_params(symbol, limit)
        response = requests.get(url=self.ORDER_BOOK_DEPTH_URL, headers=self._get_headers(), params=params)
        order_book = json.loads(response.text)
        asks = order_book['asks']
        bids = order_book['bids']
        return asks, bids

    def get_average_token_price(self, symbol, BRL_to_trade, book_side):
        time.sleep(0.1)
        token_amount = self._BRL_to_token(symbol, BRL_to_trade)
        asks, bids = self._get_order_book(symbol)
        if book_side == "asks":
            try:
                return self.price_calculator.calculate_average_price(asks, token_amount)
            except:
                return -1
        if book_side == "bids":
            try:
                return self.price_calculator.calculate_average_price(bids, token_amount)
            except:
                return -1

    def _BRL_to_token(self, symbol, BRL_to_trade):
        URL_PRICES = self.TICKER_PRICE_URL + "?symbol=%s" % symbol
        last_symbol_BRL = float(requests.get(url=URL_PRICES).json()['price'])
        symbol_amount = BRL_to_trade / last_symbol_BRL
        return symbol_amount


