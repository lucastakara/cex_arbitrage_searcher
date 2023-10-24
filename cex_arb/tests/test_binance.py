import unittest
from unittest.mock import patch

from cex_arb.entities.binance import Binance


class TestBinance(unittest.TestCase):
    def setUp(self):
        self.binance = Binance()

    @patch.object(Binance, '_request')
    def test_BRL_to_token(self, mock_request):
        # Set up the mock to return a specific response that your method under test will receive
        mock_request.return_value = {'price': '100000'}

        symbol = "BTCBRL"
        BRL_to_trade = 200

        # Call the method under test
        result = self.binance._BRL_to_token(symbol, BRL_to_trade)

        # Assert that your method behaved as expected, based on the mock data
        self.assertEqual(result, 0.002)  # This assertion is based on the mock response


if __name__ == '__main__':
    unittest.main()
