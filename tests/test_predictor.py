import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock-statistical-analysis')
from predictor import Predictor

class TestAlphaVantageWrapper(unittest.TestCase):

    def test_check_if_market_is_open(self):
        predictor = Predictor()
        is_open = predictor.check_if_market_is_open()
        print (is_open)
        # Need to change based on what time it is.


if __name__ == '__main__':
    unittest.main()
