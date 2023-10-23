import importlib.resources
import itertools
import json
import os
import time
from datetime import datetime
from multiprocessing import Queue, Process

from cex_arb.entities.binance import Binance
from cex_arb.entities.brasil_bitcoin import BrasilBitcoin
from cex_arb.slack_bot import post_message_to_slack

script_dir = os.path.dirname(__file__)

with importlib.resources.open_text("cex_arb", "tokens.json") as json_file:
    CONFIG_TOKENS = json.load(json_file)


class ArbSearcher:

    def __init__(self):
        self.cex_dict = {"Binance": Binance(),
                         "BrasilBitcoin": BrasilBitcoin()}
        self.cex_permutations = self._get_all_cex_pairs()
        self.token_brl_pairs = list(CONFIG_TOKENS["Tokens"].keys())
        self.pairs = list(itertools.product(self.token_brl_pairs, self.cex_permutations))
        self.opportunities_queue = Queue()

    def _get_all_cex_pairs(self):
        cex_list = list(self.cex_dict.keys())
        cex_permutations = list(itertools.permutations(cex_list, 2))
        return cex_permutations

    def get_opportunities(self, BRL_to_trade=40000):
        pairs_queue = Queue()
        processes = []
        opportunities = []

        for pair in self.pairs:
            pairs_queue.put(pair)
            time.sleep(0.15)

        while not pairs_queue.empty():
            token_pair = pairs_queue.get()
            searcher_process = Process(target=self.search_for_arb_opportunity, args=(token_pair, BRL_to_trade,))
            searcher_process.start()
            processes.append(searcher_process)
            time.sleep(0.2)

        for process in processes:
            process.join()

        while not self.opportunities_queue.empty():
            opportunities.append(self.opportunities_queue.get())
            time.sleep(0.15)
        return json.dumps(opportunities)

    def search_for_arb_opportunity(self, pair, BRL_to_trade):
        token_pair, exchangeA_name, exchangeB_name = pair[0], pair[1][0], pair[1][1]
        exchangeA, exchangeB = self.cex_dict[exchangeA_name], self.cex_dict[exchangeB_name]
        avg_price_cexA = exchangeA.get_average_token_price(token_pair, BRL_to_trade, "asks")
        avg_price_cexB = exchangeB.get_average_token_price(token_pair, BRL_to_trade, "bids")
        profit = avg_price_cexB - avg_price_cexA
        if profit < 0:
            time = datetime.now().strftime("%H:%M:%S")
            message = "Time: %s, Coin: %s, Exchange_Buy: %s, Exchange_Sell: %s, Profit (R$): %s" % (
                time,
                token_pair, exchangeA_name, exchangeB_name, profit)
            print(message)
            # self.opportunities_queue.put(message)
            # post_message_to_slack(message)


if __name__ == '__main__':
    arb_searcher = ArbSearcher()
    arb_searcher.get_opportunities(100)
    # while True:
    #     amount_to_trade = [2000]
    #     queue = Queue()
    #
    #     for amount in amount_to_trade:
    #         queue.put(amount)
    #         time.sleep(0.01)
    #         time.sleep(0.01)
    #
    #
    #     while not queue.empty():
    #         amount = queue.get()
    #         searcher_process = Process(target=arb_searcher.get_opportunities, args=(amount,))
    #         searcher_process.start()
    #         processes.append(searcher_process)
    #         time.sleep(0.01)
    #
    #     for process in processes:
    #         process.join()
    #         time.sleep(0.01)
    #
