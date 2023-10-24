import logging
import time

import requests

from cex_arb.utils.average_price_calculator import AveragePriceCalculator


class Binance:
    # Class constants
    API_BASE_URL = "https://api3.binance.com"
    ORDER_BOOK_DEPTH_ENDPOINT = "/api/v3/depth"
    TICKER_PRICE_ENDPOINT = "/api/v3/ticker/price"

    def __init__(self):
        # Initialize a session to reuse the same TCP connection
        self.session = requests.Session()
        # Update session headers with the default headers for the Binance API
        self.session.headers.update(self._get_default_headers())
        # Instance of the price calculator for computing average prices
        self.price_calculator = AveragePriceCalculator()

    @staticmethod
    def _get_default_headers():
        """
        Returns the default set of headers for API requests.

        :return: A dictionary containing the default headers.
        """
        return {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                          'Safari/537.36'
        }

    def _request(self, method, endpoint, max_retries=3, **kwargs):
        """
        Make an HTTP request and return the JSON response. Includes retry logic.

        :param method: HTTP method (e.g., "GET", "POST").
        :param endpoint: API endpoint (part of the URL).
        :param max_retries: Maximum number of retries in case of request failure.
        :param kwargs: Additional arguments to pass to the request (e.g., params, data, headers).
        :return: JSON response from the API as a dictionary.
        """
        for attempt in range(max_retries):
            try:
                # Attempt to make the request
                response = self.session.request(method, self.API_BASE_URL + endpoint, **kwargs)
                response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

                return response.json()  # Successful response

            except requests.exceptions.HTTPError as e:
                # Catch HTTP errors (like rate limits or server-side errors)
                print(f"HTTP error on attempt {attempt + 1}: {e}")

                if response.status_code == 429:
                    print("Rate limit reached. Waiting before retrying.")
                    time.sleep(60)  # Wait a longer time if rate-limited, adjust as necessary
                else:
                    time.sleep(2)  # Shorter wait for other kinds of HTTP errors

            except requests.exceptions.RequestException as e:
                # Catch other request-related errors
                print(f"Request failed on attempt {attempt + 1}: {e}")
                time.sleep(2)  # Wait before retrying

            except ValueError as e:
                # Catch JSON decoding errors
                print(f"JSON decoding failed on attempt {attempt + 1}: {e}")
                time.sleep(2)  # Wait before retrying

        print("All request attempts failed.")
        return None

    def _get_order_book(self, symbol, limit=200):
        """
        Retrieve the order book for a specific symbol.

        :param symbol: String representing the trading symbol (e.g., "BTCUSDT").
        :param limit: Number of orders to retrieve (default is 200).
        :return: Dictionary containing 'asks' and 'bids'.
        """
        params = {"symbol": symbol, "limit": limit}
        return self._request("GET", self.ORDER_BOOK_DEPTH_ENDPOINT, params=params)

    def get_average_token_price(self, symbol, BRL_to_trade, book_side):
        """
        Calculate the average price of a token based on the order book.

        :param symbol: String representing the trading symbol (e.g., "BTCUSDT").
        :param BRL_to_trade: The amount in BRL the user wishes to trade.
        :param book_side: String indicating which side of the order book to use ("asks" or "bids").
        :return: The calculated average price or -1 if an error occurs.
        """
        try:
            # Convert the amount in BRL to the equivalent amount in the desired token
            token_amount = self._BRL_to_token(symbol, BRL_to_trade)
            # Retrieve the order book for the specified symbol
            order_book = self._get_order_book(symbol)
            # Select the side of the order book as specified
            book = order_book['asks'] if book_side == "asks" else order_book['bids']
            # Calculate and return the average price
            return self.price_calculator.calculate_average_price(book, token_amount)
        except requests.HTTPError as http_err:
            # Log the error for debugging purposes
            logging.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
        return -1

    def _BRL_to_token(self, symbol, BRL_to_trade):
        """
        Convert an amount in Brazilian Real (BRL) to its equivalent in a specific token.

        :param symbol: String representing the trading symbol (e.g., "BTCBRL").
        :param BRL_to_trade: The amount in BRL the user wishes to trade.
        :return: The equivalent amount in the specified token.
        """
        response = self._request("GET", self.TICKER_PRICE_ENDPOINT, params={"symbol": symbol})
        last_symbol_BRL = float(response['price'])
        return BRL_to_trade / last_symbol_BRL


