import numpy as np


class AveragePriceCalculator:
    """
    A class used to calculate the average price of token orders.
    """

    def __init__(self):
        """
        Initializes the AveragePriceCalculator with empty prices and amounts.
        """
        self._initialize_order_values()

    def _initialize_order_values(self):
        """Resets the prices and amounts lists to their initial empty state."""
        self.prices = []
        self.amounts = []

    def _add_partial_order(self, price, remaining_amount):
        """
        Adds a partially consumed order to the tracking lists.

        :param price: The price of the order.
        :param remaining_amount: The remaining amount of tokens needed.
        """
        self.prices.append(price)
        self.amounts.append(remaining_amount)

    def _add_full_order(self, price, amount):
        """
        Adds a fully consumed order to the tracking lists.

        :param price: The price of the order.
        :param amount: The amount of tokens in the order.
        """
        self.prices.append(price)
        self.amounts.append(amount)

    def _add_order(self, price, amount):
        """Add an order's price and amount to the tracking lists."""
        self.prices.append(price)
        self.amounts.append(amount)

    def _reset_order_values(self):
        """Reset tracking lists for the next calculation."""
        self.prices = []
        self.amounts = []

    def calculate_average_price(self, orders, desired_amount):
        """
        Calculates the weighted average price for the desired amount of tokens.

        :param orders: A list of available orders, each represented as a list [price, amount].
        :param desired_amount: The total amount of tokens desired.
        :return: The weighted average price, or -1 if no orders are available.
        """
        if not orders:
            return -1  # No orders available

        total_acquired_amount = 0.0
        for order in orders:
            price = float(order[0])  # Convert price to float
            available_amount = float(order[1])  # Convert amount to float

            if total_acquired_amount >= desired_amount:
                break  # We have enough orders to fulfill the desired amount

            if available_amount > desired_amount - total_acquired_amount:
                # If the order satisfies the remaining desired amount, consume it partially
                amount_to_acquire = desired_amount - total_acquired_amount
                self._add_order(price, amount_to_acquire)
                total_acquired_amount = desired_amount
            else:
                # If the order is too small to satisfy the remaining amount, consume it fully
                self._add_order(price, available_amount)
                total_acquired_amount += available_amount

        if total_acquired_amount < desired_amount:
            # Not enough tokens available to satisfy the desired amount
            self._reset_order_values()  # Clean up before returning
            return -1  # Or any other indicator of inability to fulfill the request

        # Calculate the weighted average price
        weighted_avg_price = np.average(self.prices, weights=self.amounts)

        self._reset_order_values()  # Reset for the next calculation
        return weighted_avg_price
