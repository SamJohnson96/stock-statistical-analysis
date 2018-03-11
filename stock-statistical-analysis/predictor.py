import datetime
datetime.datetime.now()

class Predictor:

        def mark_prediction(self,time, predictions, stock_data):
            apple_predictions = predictions['APPLE']
            facebook_predictions = predictions['FACEBOOK']
            technology_predictions = predictions['TECHNOLOGY']
            sectors = ['apple','facebook','technology']

            # If it is hourly we need to check that markets aren't open and we stockpile news from the previous night
            if time == 'hourly':
                if check_if_market_is_open():
                    marks = {}
                    for sector in sectors:
                        is_correct = {}
                        if sector == 'apple':
                            is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(apple_predictions['NAIVE_BAYES'],stock_data),
                                                         'CHANGE' : has_changed(apple_predictions['NAIVE_BAYES']),
                                                         'DIFFERENCE' : get_movement(stock_data)}
                            is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(apple_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                    'CHANGE' : has_changed(apple_predictions['SUPPORT_VECTOR_MACHINE']),
                                                                    'DIFFERENCE' : get_movement(stock_data)}
                            is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(apple_predictions['TOTAL'],stock_data),
                                                    'CHANGE' : has_changed(apple__predictions['TOTAL']),
                                                    'DIFFERENCE' : get_movement(stock_data)}
                        elif sector == 'facebook':
                            is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(facebook_predictions['NAIVE_BAYES'],stock_data),
                                                         'CHANGE' : has_changed(facebook_predictions['TOTAL']) ,
                                                         'DIFFERENCE' : get_movement(stock_data)}
                            is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(facebook_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                    'CHANGE' : has_changed(facebook_predictions['TOTAL']),
                                                                    'DIFFERENCE' : get_movement(stock_data)}
                            is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(facebook_predictions['TOTAL'],stock_data),
                                                    'CHANGE' : has_changed(facebook_predictions['TOTAL']),
                                                    'DIFFERENCE' : get_movement(stock_data)}
                        else:
                            is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(technology_predictions['NAIVE_BAYES'],stock_data),
                                                         'CHANGE' : has_changed(technology_predictions['TOTAL']) ,
                                                         'DIFFERENCE' : get_movement(stock_data)}
                            is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(technology_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                    'CHANGE' : has_changed(technology_predictions['TOTAL']),
                                                                    'DIFFERENCE' : get_movement(stock_data)}
                            is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(technology_predictions['TOTAL'],stock_data),
                                                    'CHANGE' : has_changed(technology_predictions['TOTAL']),
                                                    'DIFFERENCE' : get_movement(stock_data)}
                        marks[sector] = is_correct
                else:
                    return None
            else:
                marks = {}
                for sector in sectors:
                    is_correct = {}
                    if sector == 'apple':
                        is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(apple_predictions['NAIVE_BAYES'],stock_data),
                                                     'CHANGE' : has_changed(apple_predictions['NAIVE_BAYES']),
                                                     'DIFFERENCE' : get_movement(stock_data)}
                        is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(apple_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                'CHANGE' : has_changed(apple_predictions['SUPPORT_VECTOR_MACHINE']),
                                                                'DIFFERENCE' : get_movement(stock_data)}
                        is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(apple_predictions['TOTAL'],stock_data),
                                                'CHANGE' : has_changed(apple__predictions['TOTAL']),
                                                'DIFFERENCE' : get_movement(stock_data)}
                    elif sector == 'facebook':
                        is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(facebook_predictions['NAIVE_BAYES'],stock_data),
                                                     'CHANGE' : has_changed(facebook_predictions['TOTAL']) ,
                                                     'DIFFERENCE' : get_movement(stock_data)}
                        is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(facebook_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                'CHANGE' : has_changed(facebook_predictions['TOTAL']),
                                                                'DIFFERENCE' : get_movement(stock_data)}
                        is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(facebook_predictions['TOTAL'],stock_data),
                                                'CHANGE' : has_changed(facebook_predictions['TOTAL']),
                                                'DIFFERENCE' : get_movement(stock_data)}
                    else:
                        is_correct['NAIVE_BAYES'] = {'CORRECT' : check_if_correct(technology_predictions['NAIVE_BAYES'],stock_data),
                                                     'CHANGE' : has_changed(technology_predictions['TOTAL']) ,
                                                     'DIFFERENCE' : get_movement(stock_data)}
                        is_correct['SUPPORT_VECTOR_MACHINE'] = {'CORRECT' : check_if_correct(technology_predictions['SUPPORT_VECTOR_MACHINE'],stock_data),
                                                                'CHANGE' : has_changed(technology_predictions['TOTAL']),
                                                                'DIFFERENCE' : get_movement(stock_data)}
                        is_correct ['TOTAL'] = {'CORRECT' : check_if_correct(technology_predictions['TOTAL'],stock_data),
                                                'CHANGE' : has_changed(technology_predictions['TOTAL']),
                                                'DIFFERENCE' : get_movement(stock_data)}
                    marks[sector] = is_correct

            return marks


        def check_if_market_is_open(self):
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

        def correlate(self,estimation):
            print ('yo dawg')
        # Get the change of stocks from the Panda files
        def get_movement(self,predictions):
            print ('yo dawg')

        def check_if_correct(self,share_or_market,prediction,stock_data):
            if share_or_market == 'facebook' or share_or_market == 'apple':
                # Do share check
                print ('yo dawg')
            else:
                # Do market check
                print('yo dawg')

        def has_changed(self, prediction):
            print ('yo dawg')
