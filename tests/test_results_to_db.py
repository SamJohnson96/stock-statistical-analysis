import unittest
import sys
import pandas as pd
import numpy
import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis')
from stock_statistical_analysis.results_to_db import ResultsToDB
from models.result import Result
from models.database_tools import Base, create_all_tables, create_new_engine, setup_database, create_new_session

class TestResultsToDB(unittest.TestCase):

    def test_push_results(self):
        # Make Result model
        now = datetime.datetime.now()
        new_result = Result(sector='test',
                            type='test',
                            machine_learning_technique='test',
                            date= now.strftime("%Y-%m-%d %H:%M"),
                            prediction= 1,
                            result= '0',
                            difference= 12.34)

        # Push result to database
        results = [new_result]
        results_to_db = ResultsToDB()
        results_to_db.push_results(results)

        # Create engine
        engine = create_new_engine('stockbot')
        Session = create_new_session(engine)
        session = Session()
        query = session.query(Result).filter(Result.sector.in_(['test'])).all()
        self.assertEqual(type(query[0]), Result)




if __name__ == '__main__':
    unittest.main()
