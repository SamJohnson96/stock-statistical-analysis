import boto3

class PredictionWrapper:

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')
    pk_key = 'sector'
    sectors = ['apple','facebook','technology']

    def get_hourly_predictions(self):
        company_predictions = {}
        for sector in self.sectors:
            predictions = {}
            response = self.table.get_item(Key={self.pk_key: sector})
            predictions['TOTAL'] = response['Item']['total_average_hourly']
            predictions['NAIVE_BAYES'] = response['Item']['naive_bayes_hourly']
            predictions['SUPPORT_VECTOR_MACHINE'] = response['Item']['support_vector_machine_hourly']
            predictions['HAS_CHANGED'] = response['Item']['hour_change']
            company_predictions[sector] = predictions
        return company_predictions

    def get_daily_predictions(self):
        company_predictions = {}
        for sector in self.sectors:
            predictions = {}
            response = self.table.get_item(Key={self.pk_key: sector})
            predictions['TOTAL'] = response['Item']['total_average_daily']
            predictions['NAIVE_BAYES'] = response['Item']['naive_bayes_daily']
            predictions['SUPPORT_VECTOR_MACHINE'] = response['Item']['support_vector_machine_daily']
            predictions['HAS_CHANGED'] = response['Item']['day_change']
            company_predictions[sector] = predictions
        return company_predictions

    def get_weekly_predictions(self):
        company_predictions = {}
        for sector in self.sectors:
            predictions = {}
            response = self.table.get_item(Key={self.pk_key: sector})
            predictions['TOTAL'] = response['Item']['total_average_weekly']
            predictions['NAIVE_BAYES'] = response['Item']['naive_bayes_weekly']
            predictions['SUPPORT_VECTOR_MACHINE'] = response['Item']['support_vector_machine_weekly']
            predictions['HAS_CHANGED'] = response['Item']['week_change']
            company_predictions[sector] = predictions
        return company_predictions

    def get_monthly_predictions(self):
        company_predictions = {}
        for sector in self.sectors:
            predictions = {}
            response = self.table.get_item(Key={self.pk_key: sector})
            predictions['TOTAL'] = response['Item']['total_average_monthly']
            predictions['NAIVE_BAYES'] = response['Item']['naive_bayes_monthly']
            predictions['SUPPORT_VECTOR_MACHINE'] = response['Item']['support_vector_machine_monthly']
            predictions['HAS_CHANGED'] = response['Item']['month_change']
            company_predictions[sector] = predictions
        return company_predictions


    def reset_hour_change(self):
        for sector in self.sectors:
            self.table.update_item(
                Key={
                    self.pk_key: sector,
                },
                UpdateExpression='SET hour_change = :val1',
                ExpressionAttributeValues={
                    ':val1': 0
                }
            )

    def reset_day_change(self):
        for sector in self.sectors:
            self.table.update_item(
                Key={
                    self.pk_key: sector,
                },
                UpdateExpression='SET day_change = :val1',
                ExpressionAttributeValues={
                    ':val1': 0
                }
            )

    def reset_week_change(self):
        for sector in self.sectors:
            self.table.update_item(
                Key={
                    self.pk_key: sector,
                },
                UpdateExpression='SET week_change = :val1',
                ExpressionAttributeValues={
                    ':val1': 0
                }
            )

    def reset_month_change(self):
        for sector in self.sectors:
            self.table.update_item(
                Key={
                    self.pk_key: sector,
                },
                UpdateExpression='SET month_change = :val1',
                ExpressionAttributeValues={
                    ':val1': 0
                }
            )
