import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock_statistical_analysis')
from alpha_vantage_wrapper import AlphaVantage

class TestAlphaVantageWrapper(unittest.TestCase):

    def test_get_intraday(self):
        wrapper = AlphaVantage()
        data = wrapper.get_intraday()
        data = data.tail(1)
        for row in data.iterrows():
            open_price = row[1][0]
            close_price = row [1][3]
        self.assertEqual(type(open_price),numpy.float64)
        self.assertEqual(type(close_price),numpy.float64)

    def test_get_days_information(self):
        wrapper = AlphaVantage()
        data = wrapper.get_days_information()
        data = data.tail(1)
        for row in data.iterrows():
            open_price = row[1][0]
            close_price = row [1][3]
        self.assertEqual(type(open_price),numpy.float64)
        self.assertEqual(type(close_price),numpy.float64)

    def test_get_weekly_information(self):
        wrapper = AlphaVantage()
        data = wrapper.get_weekly_information()
        data = data.tail(1)
        for row in data.iterrows():
            open_price = row[1][0]
            close_price = row [1][3]
        self.assertEqual(type(open_price),numpy.float64)
        self.assertEqual(type(close_price),numpy.float64)

    def test_get_monthly_information(self):
        wrapper = AlphaVantage()
        data = wrapper.get_monthly_information()
        data = data.tail(1)
        for row in data.iterrows():
            open_price = row[1][0]
            close_price = row [1][3]
        self.assertEqual(type(open_price),numpy.float64)
        self.assertEqual(type(close_price),numpy.float64)

    def test_get_sector_intraday(self):
        wrapper = AlphaVantage()
        data = wrapper.get_sector_intraday()
        self.assertEqual(type(data),numpy.float64)

    def test_get_sector_daily(self):
        wrapper = AlphaVantage()
        data = wrapper.get_sector_daily()
        self.assertEqual(type(data),numpy.float64)

    def test_get_sector_weekly(self):
        wrapper = AlphaVantage()
        data = wrapper.get_sector_weekly()
        self.assertEqual(type(data),numpy.float64)

    def test_get_sector_monthly(self):
        wrapper = AlphaVantage()
        data = wrapper.get_sector_monthly()
        self.assertEqual(type(data),numpy.float64)


if __name__ == '__main__':
    unittest.main()
