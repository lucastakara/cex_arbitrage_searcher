import unittest
import numpy as np
from cex_arb.utils.average_price_calculator import \
    AveragePriceCalculator


class TestAveragePriceCalculator(unittest.TestCase):

    def setUp(self):
        """Create an instance of AveragePriceCalculator before each test."""
        self.calculator = AveragePriceCalculator()

    def test_initial_state(self):
        """Test the initial state of the calculator."""
        self.assertEqual(self.calculator.prices, [])
        self.assertEqual(self.calculator.amounts, [])

    def test_no_orders(self):
        """Test the average price calculation when there are no orders."""
        self.assertEqual(self.calculator.calculate_average_price([], 100), -1)

    def test_average_price_with_partial_order(self):
        """Test the average price calculation when the last order is partially consumed."""
        orders = [[10, 50], [20, 70]]  # price, amount
        desired_amount = 80
        expected_average_price = (10 * 50 + 20 * 30) / 80  # (price*amount + price*remaining_amount) / desired_amount
        self.assertEqual(self.calculator.calculate_average_price(orders, desired_amount), expected_average_price)

    def test_average_price_with_full_orders(self):
        """Test the average price calculation when all orders are fully consumed."""
        orders = [[10, 50], [15, 30], [20, 20]]  # price, amount
        desired_amount = 100
        expected_average_price = np.average([10, 15, 20], weights=[50, 30, 20])  # weighted average
        self.assertEqual(self.calculator.calculate_average_price(orders, desired_amount), expected_average_price)

    def test_reset_after_calculation(self):
        """Test if the calculator resets its state after a calculation."""
        orders = [[10, 50]]
        self.calculator.calculate_average_price(orders, 30)
        self.assertEqual(self.calculator.prices, [])  # should be reset to []
        self.assertEqual(self.calculator.amounts, [])  # should be reset to []


if __name__ == '__main__':
    unittest.main()
