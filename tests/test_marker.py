import unittest
import sys
import pandas as pd
import numpy
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/stock_statistical_analysis')
from marker import Marker

class TestMarker(unittest.TestCase):

    def test_get_marks(self):
        marker = Marker()
        self.assertTrue(marker.check_if_correct(0,0))
        self.assertTrue(marker.check_if_correct(1,1))
        self.assertFalse(marker.check_if_correct(0,1))
        self.assertFalse(marker.check_if_correct(1,0))




if __name__ == '__main__':
    unittest.main()
