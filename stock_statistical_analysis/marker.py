import datetime
import sys
from stock_calculator import StockCalculator
sys.path.insert(0, '/Users/sam/workspace/final_year_project/stock_statistical_analysis/')
from models.result import Result

class Marker:

    stock_calculator = StockCalculator()

    def get_marks(self,sector,type_of_result,predictions,stock_data):
        stock_movement,difference = self.stock_calculator.stock_movement(stock_data.tail(1))
        keys = list(predictions.keys())
        results = []
        for key in keys:
            check_if_correct = self.check_if_correct(predictions[key],stock_movement)
            now = datetime.datetime.now()
            new_result = Result(sector=sector,type=type_of_result,machine_learning_technique=key,date=now.strftime("%Y-%m-%d %H:%M"),prediction=predictions[key],result=check_if_correct,difference=difference)
            results.append(new_result)
        return results

    def check_if_correct(self,prediction, stock_movement):
        if stock_movement == prediction:
            return True
        else:
            return False
