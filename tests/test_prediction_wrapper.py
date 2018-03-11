import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock-statistical-analysis')
from prediction_wrapper import PredictionWrapper
from decimal import *

class TestPredictionWrapper(unittest.TestCase):

    def test_get_hourly_predictions(self):
        wrapper = PredictionWrapper()
        hour = wrapper.get_hourly_predictions()
        self.assertEqual(list(hour.keys()),['apple','facebook','technology'])
        self.assertEqual(type(hour['apple']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(hour['apple']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(hour['apple']['TOTAL']),Decimal)
        self.assertEqual(type(hour['facebook']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(hour['facebook']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(hour['facebook']['TOTAL']),Decimal)
        self.assertEqual(type(hour['technology']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(hour['technology']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(hour['technology']['TOTAL']),Decimal)


    def test_get_daily_predictions(self):
        wrapper = PredictionWrapper()
        day = wrapper.get_daily_predictions()
        self.assertEqual(list(day.keys()),['apple','facebook','technology'])
        self.assertEqual(type(day['apple']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(day['apple']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(day['apple']['TOTAL']),Decimal)
        self.assertEqual(type(day['facebook']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(day['facebook']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(day['facebook']['TOTAL']),Decimal)
        self.assertEqual(type(day['technology']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(day['technology']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(day['technology']['TOTAL']),Decimal)

    def test_get_weekly_predictions(self):
        wrapper = PredictionWrapper()
        week = wrapper.get_weekly_predictions()
        self.assertEqual(list(week.keys()),['apple','facebook','technology'])
        self.assertEqual(type(week['apple']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(week['apple']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(week['apple']['TOTAL']),Decimal)
        self.assertEqual(type(week['facebook']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(week['facebook']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(week['facebook']['TOTAL']),Decimal)
        self.assertEqual(type(week['technology']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(week['technology']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(week['technology']['TOTAL']),Decimal)

    def test_get_monthly_predictions(self):
        wrapper = PredictionWrapper()
        month = wrapper.get_monthly_predictions()
        self.assertEqual(list(month.keys()),['apple','facebook','technology'])
        self.assertEqual(type(month['apple']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(month['apple']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(month['apple']['TOTAL']),Decimal)
        self.assertEqual(type(month['facebook']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(month['facebook']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(month['facebook']['TOTAL']),Decimal)
        self.assertEqual(type(month['technology']['SUPPORT_VECTOR_MACHINE']),Decimal)
        self.assertEqual(type(month['technology']['NAIVE_BAYES']),Decimal)
        self.assertEqual(type(month['technology']['TOTAL']),Decimal)


if __name__ == '__main__':
    unittest.main()
