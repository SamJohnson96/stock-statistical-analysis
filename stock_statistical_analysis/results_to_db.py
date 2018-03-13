import sys
from sqlalchemy import Column, Integer, String, Float
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/')
from models.result import Result
from models.database_tools import Base, create_all_tables, create_new_engine, setup_database, create_new_session

class ResultsToDB:

    def push_results(self,results):
        engine = create_new_engine('stockbot')
        Session = create_new_session(engine)
        session = Session()
        session.bulk_save_objects(results)
        session.commit()
