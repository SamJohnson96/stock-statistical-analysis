import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock-statistical-analysis')
from alpha_vantage_wrapper import AlphaVantage

class TestAlphaVantageWrapper(unittest.TestCase):

    def test_get_intraday(self):
        wrapper = AlphaVantage()
        data ,meta_data = wrapper.get_intraday()
        self.assertEqual(meta_data['1. Information'],'Intraday (60min) prices and volumes')
        self.assertEqual(meta_data['2. Symbol'],'AAPL')

    def test_get_daily(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_daily()
        self.assertEqual(meta_data['1. Information'],'Daily Prices (open, high, low, close) and Volumes')
        self.assertEqual(meta_data['2. Symbol'],'AAPL')

    def test_get_weekly(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_weekly()
        self.assertEqual(meta_data['1. Information'],'Weekly Prices (open, high, low, close) and Volumes')
        self.assertEqual(meta_data['2. Symbol'],'AAPL')

    def test_get_monthly(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_monthly()
        self.assertEqual(meta_data['1. Information'],'Monthly Prices (open, high, low, close) and Volumes')
        self.assertEqual(meta_data['2. Symbol'],'AAPL')

    def test_get_sector_intraday(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_sector_intraday()
        self.assertEqual(type(data),numpy.float64)
        self.assertEqual(meta_data['Information'],'US Sector Performance (realtime & historical)')

    def test_get_sector_daily(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_sector_daily()
        self.assertEqual(type(data),numpy.float64)
        self.assertEqual(meta_data['Information'],'US Sector Performance (realtime & historical)')

    def test_get_sector_weekly(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_sector_weekly()
        self.assertEqual(type(data),numpy.float64)
        self.assertEqual(meta_data['Information'],'US Sector Performance (realtime & historical)')

    def test_get_sector_monthly(self):
        wrapper = AlphaVantage()
        data,meta_data = wrapper.get_sector_monthly()
        self.assertEqual(type(data),numpy.float64)
        self.assertEqual(meta_data['Information'],'US Sector Performance (realtime & historical)')

if __name__ == '__main__':
    unittest.main()
