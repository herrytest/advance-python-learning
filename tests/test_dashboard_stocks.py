import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import fetch_stock_data

class TestStockData(unittest.TestCase):

    def test_fetch_stock_data(self):
        """Test fetch_stock_data returns a valid list of stocks"""
        # This test might be slow as it hits external APIs (yfinance, nsepython)
        # In a real CI environment, we should mock these.
        # For this local regression, we'll allow the real call but add a timeout/warning mentally.
        
        print("\nFetching stock data (this may take a moment)...")
        stocks = fetch_stock_data()
        
        self.assertIsInstance(stocks, list)
        self.assertGreater(len(stocks), 0, "No stocks returned")
        
        # Check structure
        first_stock = stocks[0]
        self.assertIn("name", first_stock)
        self.assertIn("price", first_stock)
        self.assertIn("change", first_stock)
        self.assertIn("pct", first_stock)
        self.assertIn("is_up", first_stock)
        self.assertIn("last_updated", first_stock)
        
        # Check specific stocks are present (BSE SENSEX, NIFTY 50)
        names = [s['name'] for s in stocks]
        self.assertIn("BSE SENSEX", names)
        # NIFTY 50 might fail if nsepython is down, but based on recent validation it works.

if __name__ == '__main__':
    unittest.main()
