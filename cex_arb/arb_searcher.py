import importlib.resources as pkg_resources
import itertools
import json
from datetime import datetime
from multiprocessing import Process, Manager

from cex_arb.entities.binance import Binance
from cex_arb.entities.brasil_bitcoin import BrasilBitcoin

from cex_arb import utils


class ArbitrageOpportunityFinder:
    def __init__(self):
        """
        Initialize the ArbitrageOpportunityFinder with specific exchange entities and load token pairs.
        """
        self.exchange_entities = {
            "Binance": Binance(),
            "BrasilBitcoin": BrasilBitcoin()
        }
        self.token_pairs = self._load_token_pairs()
        self.exchange_permutations = self._generate_exchange_permutations()

    @staticmethod
    def _load_token_pairs():
        """
        Load trading pairs from a JSON configuration file.

        :return: A list of trading pairs (e.g., ['BTCUSD', 'ETHUSD']).
        """
        with pkg_resources.open_text(utils, 'tokens.json') as tokens_file:
            tokens = json.load(tokens_file)
        return list(tokens["Tokens"].keys())

    def _generate_exchange_permutations(self):
        """
        Generate all possible ordered combinations of exchanges (permutations).

        :return: A list of tuples representing permutations of exchanges.
        """
        exchange_names = list(self.exchange_entities.keys())
        return list(itertools.permutations(exchange_names, 2))

    @staticmethod
    def _calculate_profit(pair, BRL_to_trade, results, exchange_entities):
        """
        Calculate potential profit from arbitrage between two exchanges and add the opportunity to the results if profitable.

        :param pair: A tuple containing the token pair and a tuple of exchange names (e.g., ('BTCUSD', ('Binance', 'BrasilBitcoin'))).
        :param BRL_to_trade: The amount in BRL intended for trade.
        :param results: A shared list between processes to store profitable opportunities.
        :param exchange_entities: A dictionary containing initialized exchange entities.
        """
        token_pair, (buy_exchange_name, sell_exchange_name) = pair
        buy_exchange = exchange_entities[buy_exchange_name]
        sell_exchange = exchange_entities[sell_exchange_name]

        buy_price = buy_exchange.get_average_token_price(token_pair, BRL_to_trade, "asks")
        sell_price = sell_exchange.get_average_token_price(token_pair, BRL_to_trade, "bids")

        profit = sell_price - buy_price
        if profit < 0:
            opportunity = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "coin": token_pair,
                "exchange_buy": buy_exchange_name,
                "exchange_sell": sell_exchange_name,
                "profit": f'R${profit:.2f}'  # Formatting profit to 2 decimal places
            }
            results.append(opportunity)

    def find_opportunities(self, BRL_to_trade=40000):
        """
        Find and return arbitrage opportunities.

        :param BRL_to_trade: The amount in BRL that the trader intends to use (default is 40000).
        :return: A JSON string representing a list of arbitrage opportunities.
        """
        with Manager() as manager:
            opportunities = manager.list()
            processes = []

            for pair in itertools.product(self.token_pairs, self.exchange_permutations):
                process = Process(target=self._calculate_profit, args=(pair, BRL_to_trade, opportunities, self.exchange_entities))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()

            return json.dumps(list(opportunities)) if opportunities else json.dumps([])

