import numpy as np


class AveragePriceCalculator:

    def __init__(self):
        self.prices = []
        self.amounts = []
        self._reset_values()

    def _reset_values(self):
        self.prices = []
        self.amounts = []

    def _consume_large_order_partially(self, order, token_amount):
        self.prices.append(float(order[0]))
        self.amounts.append(float(token_amount - sum(self.amounts)))

    def _consume_small_order(self, order):
        self.prices.append(float(order[0]))
        self.amounts.append(float(order[1]))

    def calculate_average_price(self, orders, token_amount):
        if len(orders) == 0:
            return -1

        while not (sum(self.amounts) >= float(token_amount)):
            order = orders[0]
            if float(order[1]) > token_amount:
                self._consume_large_order_partially(order, token_amount)
            else:
                self._consume_small_order(order)
            orders.pop(0)

        avg_price = np.average(np.array(self.prices), weights=np.array(self.amounts))
        self._reset_values()
        return avg_price
