import argparse
import sys
import datetime
from alpha_vantage_wrapper import AlphaVantage
from prediction_wrapper import PredictionWrapper
from marker import Marker
from results_to_db import ResultsToDB

prediction_wrapper = PredictionWrapper()
alpha_vantage_wrapper = AlphaVantage()
marker = Marker()
results_to_db = ResultsToDB()

class TimedOut(Exception):
  pass

def build_args():
    """Method that builds arguments to use in the command line
    Returns:
         ArgumentParser

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--hour", help="Handle new predictions within the last hour",
                    action="store_true")
    parser.add_argument("-d", "--day", help="Handle new predictions for the last day",
                    action="store_true")
    parser.add_argument("-w", "--week", help="Handle new predictions for the last week",
                    action="store_true")
    parser.add_argument("-m", "--month", help="Handle new predictions for the last month",
                    action="store_true")
    return parser

def handle_hourly(attempt=0):
    if attempt < 5:
        if check_if_market_is_open():
            # Get hourly predictions of technology, facebook & apple
            predictions = prediction_wrapper.get_hourly_predictions()

            # Get what has been happenining over the last hour.
            try:
                stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('hour')
            except TimedOut as e:
                print ("Alpha Vantage did not return anything, trying again")
                handle_hourly(attempt+1)

            # Extract information and mark it.
            sectors = ['apple','facebook','technology']
            results = []
            for sector in sectors:
                print ('-- Getting ML predictions --')
                prediction = predictions[sector]
                print ('-- Getting Stock Data for %s --' % sector)
                sector_stock = stock_data[sector]
                print ('-- Marking whether prediction is true or not --')
                results.append(marker.get_marks(sector,'hour',prediction,sector_stock))
                print ('-- Push to database --')
            # Flatten results & push to db
            results = [item for sublist in results for item in sublist]
            results_to_db.push_results(results)
            prediction_wrapper.reset_hour_change()
        else:
            print ('--- Market is not open ---')
    else:
        print('--- Predictions failed to be marked, Alpha Vantage not responding ---')
        return;



def handle_daily():
    # Get daily predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_daily_predictions()
    # Get what has been happenining over the last hour.
    stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('day')
    #Extract information and mark it.
    sectors = ['apple','facebook','technology']
    results = []
    for sector in sectors:
        print ('-- Getting ML predictions --')
        prediction = predictions[sector]
        print ('-- Getting Stock Data for %s --' % sector)
        sector_stock = stock_data[sector]
        print ('-- Marking whether prediction is true or not --')
        results.append(marker.get_marks(sector,'day',prediction,sector_stock))
        print ('-- Push to database --')
    results = [item for sublist in results for item in sublist]
    results_to_db.push_results(results)
    prediction_wrapper.reset_day_change()

def handle_weekly():
    # Get weekly predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_weekly_predictions()

    # Get what has been happenining over the last hour.
    stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('week')

    # Extract information and mark it.
    sectors = ['apple','facebook','technology']
    results = []
    for sector in sectors:
        print ('-- Getting ML predictions --')
        prediction = predictions[sector]
        print ('-- Getting Stock Data for %s --' % sector)
        sector_stock = stock_data[sector]
        print ('-- Marking whether prediction is true or not --')
        results.append(marker.get_marks(sector,'week',prediction,sector_stock))
        print ('-- Push to database --')

    results = [item for sublist in results for item in sublist]
    results_to_db.push_results(results)
    prediction_wrapper.reset_week_change()


def handle_monthly():
    # Get monthly predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_monthly_predictions()

    # Get what has been happenining over the last hour.
    stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('month')

    # Extract information and mark it.
    sectors = ['apple','facebook','technology']
    results = []
    for sector in sectors:
        print ('-- Getting ML predictions --')
        prediction = predictions[sector]
        print ('-- Getting Stock Data for %s --' % sector)
        sector_stock = stock_data[sector]
        print ('-- Marking whether prediction is true or not --')
        results.append(marker.get_marks(sector,'month',prediction,sector_stock))
        print ('-- Push to database --')

    results = [item for sublist in results for item in sublist]
    results_to_db.push_results(results)
    prediction_wrapper.reset_month_change()

def check_if_market_is_open():
    time = datetime.datetime.now()
    if time.hour < 13:
        return False
    elif time.hour > 20:
        return False
    elif time.minute < 30 and time.hour == 13:
        return False
    elif time.minute > 30 and time.hour == 20:
        return False
    else:
        return True

if __name__ == "__main__":

    parser = build_args()
    args = parser.parse_args()

    # Choose what to do using arguments from command line
    if args.hour:
        try:
            handle_hourly()
    elif args.day:
        try:
            handle_daily()
    elif args.week:
        try:
            handle_weekly()
    elif args.month:
        try:
            handle_monthly()
