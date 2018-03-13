import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/')
from models.result import Result
from stock_statistical_analysis.marker import Marker
from stock_statistical_analysis.prediction_wrapper import PredictionWrapper
from stock_statistical_analysis.alpha_vantage_wrapper import AlphaVantage

class TestMarker(unittest.TestCase):

    def test_get_marks(self):
        marker = Marker()
        prediction_wrapper = PredictionWrapper()
        alpha_vantage_wrapper = AlphaVantage()

        predictions = prediction_wrapper.get_hourly_predictions()
        apple_predictions = predictions['apple']
        stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('hour')
        apple_stock_data = stock_data['apple']

        result = marker.get_marks('apple','hour',apple_predictions,apple_stock_data)

        for mark in result:
            self.assertTrue(type(mark), Result)


    def test_check_if_correct(self):
        marker = Marker()
        self.assertTrue(marker.check_if_correct(0,0))
        self.assertTrue(marker.check_if_correct(1,1))
        self.assertFalse(marker.check_if_correct(0,1))
        self.assertFalse(marker.check_if_correct(1,0))




if __name__ == '__main__':
    unittest.main()
