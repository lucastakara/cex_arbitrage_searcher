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
    def _request(url, max_retries=3):
        """
        Perform a request and handle exceptions gracefully. Retry up to max_retries if the request fails.
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    print("Rate limit reached. Waiting before retrying.")
                    time.sleep(60)  # for example, wait for 60 seconds
                else:
                    print(f"HTTP error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            except ValueError as e:  # Includes JSONDecodeError
                print(f"Response is not JSON or no data: {e}")

            # If we haven't returned by this point, we've caught an exception, so wait and try again
            print(f"Attempt {attempt + 1} failed, retrying in 2 seconds...")
            time.sleep(2)

        # After all retries, return None to indicate failure
        return None

    def _BRL_to_token(self, symbol, BRL_to_trade):
        URL_PRICES = "https://brasilbitcoin.com.br/API/prices/%s" % symbol
        response_data = self._request(URL_PRICES)
        if response_data:
            last_symbol_BRL = float(response_data.get('last', 0))  # Default to 0 if 'last' is not present
            symbol_amount = BRL_to_trade / last_symbol_BRL
            return symbol_amount
        else:
            print("All attempts to fetch data failed.")
            return None

    @staticmethod
    def manipulate_order_book(data):
        new_data = []
        for order in data:
            new_data.append([order['preco'], order['quantidade']])
        return new_data

# print(brasil_bitcoin.get_average_token_price("BTC", 40000, "asks"))
