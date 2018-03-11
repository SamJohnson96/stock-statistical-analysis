import alpha_vantage_wrapper
import prediction_wrapper
import predictor
import argparse

prediction_wrapper = PredictionWrapper()
alpha_vantage_wrapper = AlphaVantageWrapper()
predictor = Predictor()

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

def handle_hourly():
    # Get hourly predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_hourly_predictions()

    # Get what has been happenining over the last hour.
    stock_data = alpha_vantage_wrapper.create_dictionary_of_prices('hour')

    # See if there was a new prediction given and mark flag if needed to.
    predictor.correct_prediction('hour',predictions,stock_data)


def handle_daily():
    # Get daily predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_daily_predictions()

    # Get what has been happenining over the last hour.
    alpha_vantage_wrapper.create_dictionary_of_prices('day')

    # See if there was a new prediction given and mark flag if needed to.

    # Update database if correct or not - Mark with what gain was given.

def handle_weekly():
    # Get weekly predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_weekly_predictions()

    # Get what has been happenining over the last hour.
    alpha_vantage_wrapper.create_dictionary_of_prices('week')

    # See if there was a new prediction given and mark flag if needed to.

    # Update database if correct or not - Mark with what gain was given.


def handle_monthly():
    # Get monthly predictions of technology, facebook & apple
    predictions = prediction_wrapper.get_monthly_predictions()

    # Get what has been happenining over the last hour.
    alpha_vantage_wrapper.create_dictionary_of_prices('month')

    # See if there was a new prediction given and mark flag if needed to.

    # Update database if correct or not - Mark with what gain was given.


if __name__ == "__main__":

    parser = build_args()
    args = parser.parse_args()

    # Choose what to do using arguments from command line
    if args.hour:
        handle_hourly()
    elif args.day:
        handle_daily()
    elif args.week:
        handle_weekly()
    elif args.month:
        handle_monthly()
