import unittest
from cex_arb.arb_searcher import ArbitrageOpportunityFinder


class TestArbitrageOpportunityFinder(unittest.TestCase):

    def setUp(self):
        """Perform setup for the tests; this function is called before each test function."""
        self.arb_finder = ArbitrageOpportunityFinder()
        self.mock_brl_to_trade = 40000  # Example amount

    def test_init(self):
        """Test the initialization of the ArbitrageOpportunityFinder instance."""
        self.assertIsNotNone(self.arb_finder.exchange_entities)
        self.assertTrue('Binance' in self.arb_finder.exchange_entities)

    def test_load_token_pairs(self):
        """Test the _load_token_pairs method."""
        tokens = self.arb_finder._load_token_pairs()
        expected_tokens = ['BTCBRL', 'ETHBRL', 'ADABRL', 'LTCBRL', 'XRPBRL', 'DOGEBRL', 'SOLBRL']
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
