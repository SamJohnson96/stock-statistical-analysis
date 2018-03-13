import pandas as pd

class StockCalculator:

    def stock_movement(self,stock_data):
        for row in stock_data.iterrows():
            open_price = row[1][0]
            close_price = row[1][3]
            difference = close_price - open_price
            if difference > 0:
                return 1,difference
            else:
                return 0,difference
