import imp
import json
import sys
import boto3
import time
from datetime import datetime
from collections import Counter
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            article_id = record['dynamodb']['NewImage']['article_id']['N']
        else:
            print('Not a new event.')
            return;
    article = wait_for_all_classifications(article_id, 0)
    if article is None:
        print ('Issue with collecting classifications')
    else:
        update_hour(article)
        update_day(article)
        update_week(article)
        update_month(article)


def wait_for_all_classifications(article_id, retry):
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('technology_article_results')
    pk_key = 'article_id'

    # Get row
    response = table.get_item(Key={pk_key: int(article_id)})
    article = response['Item']

    if 'naive_bayes' in article.keys() and 'support_vector_machine' in article.keys():
        return article
    elif retry < 5:
        #If they're not all there then wait.
        time.sleep(3)
        return wait_for_all_classifications(article_id,retry+1)
    else:
        return None


def update_hour(article):
    print('--- Updating hour ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('technology_article_results')

    article_id = article['article_id']
    hour_ago = article_id - 3600

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(hour_ago),int(article_id))
                )

    svm_classification = article['naive_bayes']
    naive_bayes_classification = article['naive_bayes']

    update_svm_classification('hour',response,svm_classification)
    update_naive_bayes_classification('hour',response,naive_bayes_classification)
    update_average('hour',response,naive_bayes_classification, svm_classification)
    mark_as_changed('hour')

def update_day(article):
    print('--- Updating day ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('technology_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - (24*3600)

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    naive_bayes_classification = article['naive_bayes']

    update_svm_classification('day',response,svm_classification)
    update_naive_bayes_classification('day',response,naive_bayes_classification)
    update_average('day',response,naive_bayes_classification, svm_classification)
    mark_as_changed('day')

def update_week(article):
    print('--- Updating week ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('technology_article_results')

    article_id = article['article_id']
    a_week_ago = article_id - (7*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(a_week_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    naive_bayes_classification = article['naive_bayes']
    
    update_svm_classification('week',response,svm_classification)
    update_naive_bayes_classification('week',response,naive_bayes_classification)
    update_average('week',response,naive_bayes_classification, svm_classification)
    mark_as_changed('week')

def update_month(article):
    print('--- Updating hour ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('technology_article_results')

    article_id = article['article_id']
    a_month_ago = article_id - (31*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(a_month_ago),int(article_id))
             )

    # Get classifcations from the given prediction table
    svm_classification = article['naive_bayes']
    naive_bayes_classification = article['naive_bayes']

    # Update the tables according to the result and mark as changed.
    update_svm_classification('month',response,svm_classification)
    update_naive_bayes_classification('month',response,naive_bayes_classification)
    update_average('month',response,naive_bayes_classification, svm_classification)
    mark_as_changed('month')

def update_svm_classification(measure, results, new_classification):
    print('--- Updating SVM for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    svm_classification = []
    svm_classification.append(new_classification)
    for result in results:
        svm_classification.append(result['naive_bayes'])
    updated_prediction = get_highest_freq(svm_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET support_vector_machine_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET support_vector_machine_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET support_vector_machine_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET support_vector_machine_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )



def update_naive_bayes_classification(measure, results, new_classification):
    print('--- Updating Naive Bayes for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    support_vector_machine_classification = []
    support_vector_machine_classification.append(new_classification)
    for result in results:
        support_vector_machine_classification.append(result['naive_bayes'])
    updated_prediction = get_highest_freq(support_vector_machine_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET naive_bayes_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET naive_bayes_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET naive_bayes_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET naive_bayes_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )

def update_average(measure, results, naive_bayes, svm_classification):
    print('--- Updating Total Average for %s ---' % measure)
    results = results['Items']
    all_classification = []
    all_classification.append(naive_bayes)
    all_classification.append(svm_classification)
    for result in results:
        all_classification.append(result['naive_bayes'])
        all_classification.append(result['support_vector_machine'])

    updated_prediction = get_highest_freq(all_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET total_average_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET total_average_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET total_average_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET total_average_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )

def get_highest_freq(classifications):
    most_common,num_most_common = Counter(classifications).most_common(1)[0]
    return most_common

def mark_as_changed(time_interval):
    if 'hour':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET hour_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif 'day':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET day_chance = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif 'week':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET week_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif 'month':
        table.update_item(
            Key={
                'sector': 'technology',
            },
            UpdateExpression='SET month_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
