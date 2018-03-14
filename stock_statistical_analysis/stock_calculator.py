import pandas as pd

class StockCalculator:

    def stock_movement(self,stock_data,sector="company"):
        if sector != 'technology':
            for row in stock_data.iterrows():
                open_price = row[1][0]
                close_price = row[1][3]
                difference = close_price - open_price
                if difference > 0:
                    return 1,difference
                else:
                    return 0,difference
        else:
                if stock_data > 0:
                    return 1,stock_data
                else:
                    return 0,stock_data
