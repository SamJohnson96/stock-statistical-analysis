import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock_statistical_analysis')
from stock_calculator import StockCalculator
from alpha_vantage_wrapper import AlphaVantage

class TestStockCalculator(unittest.TestCase):

    def test_stock_movement(self):
        alpha_vantage_wrapper = AlphaVantage()
        prices = alpha_vantage_wrapper.create_dictionary_of_prices('day')
        apple_prices = prices['apple']
        stock_calculator = StockCalculator()
        movement = stock_calculator.stock_movement(apple_prices)
        self.assertEqual(type(movement),tuple)
        self.assertEqual(type(movement[0]),int)
        self.assertEqual(type(movement[1]), numpy.float64)

if __name__ == '__main__':
    unittest.main()
