import imp
import json
import sys
import boto3
import time
import numpy as np
from datetime import datetime

def lambda_handler(event, context):
    article_id = get_new_article_id(event)
    article = wait_for_all_classifications(article_id, 0)
    if article is None:
        print ('Issue with collecting classifications')
    else:
        update_hour(article)
        update_day(article)
        update_week(article)
        update_month(article)

def get_new_article_id(event):
    article = []
    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            article['article_id'] = record['dynamodb']['NewImage']['article_id']['N']
        else:
            print('Not a new event.')
            return;

def wait_for_all_classifications(article_id, retry):
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = 'apple_article_results'
    pk_key = 'article_id'

    # Get row
    response = table.get_item(Key={pk_key: int(article_id)})
    article = response['Item']

    if 'naive_bayes' in response.keys() and 'support_vector_machine' in response.keys():
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
    table = dynamodb.Table('apple_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - 3600

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    update_svm_classification('hour',response,svm_classification)

    # Get Naive Bayes classification
    naive_bayes_classification = article['naive_bayes']
    update_naive_bayes_classification('hour',response,naive_bayes_classification)

    # Work out average classification
    average_prediction = get_average('hour',response,naive_bayes_classification, svm_classification)

def update_day(article):
    print('--- Updating day ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - (24*3600)

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    update_svm_classification('day',response,svm_classification)

    # Get Naive Bayes classification
    naive_bayes_classification = article['naive_bayes']
    update_naive_bayes_classification('day',response,naive_bayes_classification)

    # Work out average classification
    average_prediction = get_average('day',response,naive_bayes_classification, svm_classification)

def update_week(article):
    print('--- Updating week ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - (7*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    update_svm_classification('week',response,svm_classification)

    # Get Naive Bayes classification
    naive_bayes_classification = article['naive_bayes']
    update_naive_bayes_classification('week',response,naive_bayes_classification)

    # Work out average classification
    average_prediction = get_average('week',response,naive_bayes_classification, svm_classification)

def update_month(article):
    print('--- Updating hour ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - (31*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get SVM classification
    svm_classification = article['naive_bayes']
    update_svm_classification('month',response,svm_classification)

    # Get Naive Bayes classification
    naive_bayes_classification = article['naive_bayes']
    update_naive_bayes_classification('month',response,naive_bayes_classification)

    # Work out average classification
    average_prediction = update_average('month',response,  naive_bayes_classification, svm_classification)

def update_svm_classification(measure, results, new_classification):
    results = results['Items']
    #Go through each result and get svm classification row
    svm_classification = []
    svm_classification.append(new_classification)
    for result in results:
        svm_classification.append(result['naive_bayes'])
    updated_prediction = get_highest_freq(svm_classification)

    if measure == 'hour':
        row = 'naive_bayes_hourly'
    elif measure == 'day':
        row = 'naive_bayes_daily'
    elif measure == 'week':
        row = 'naive_bayes_weekly'
    elif measure == 'month':
        row = 'naive_bayes_monthly'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')
    table.update_item(
        Key={
            'sector': 'apple',
        },
        UpdateExpression='SET :val1 = :val2',
        ExpressionAttributeValues={
            ':val1': row
            ':val2': int(updated_prediction)
        }
    )

def update_naive_bayes_classification(measure, results, new_classification):
    results = results['Items']
    #Go through each result and get svm classification row
    naive_bayes_classification = []
    naive_bayes_classification.append(new_classification)
    for result in results:
        naive_bayes_classification.append(result['naive_bayes'])
    updated_prediction = get_highest_freq(naive_bayes_classification)

    if measure == 'hour':
        row = 'naive_bayes_hourly'
    elif measure == 'day':
        row = 'naive_bayes_daily'
    elif measure == 'week':
        row = 'naive_bayes_weekly'
    elif measure == 'month':
        row = 'naive_bayes_monthly'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')
    table.update_item(
        Key={
            'sector': 'apple',
        },
        UpdateExpression='SET :val1 = :val2',
        ExpressionAttributeValues={
            ':val1': row
            ':val2': int(updated_prediction)
        }
    )

def update_average(measure, results, naive_bayes, svm_classification):
    results = results['Items']
    #Go through each result and get svm classification row
    all_classification = []
    all_classification.append(naive_bayes)
    all_classification.append(svm_classification)
    for result in results:
        all_classification.append(result['naive_bayes'])
        all_classification.append(result['support_vector_machine'])

    updated_prediction = get_highest_freq(all_classification)

    if measure == 'hour':
        row = 'total_average_hourly'
    elif measure == 'day':
        row = 'total_average_daily'
    elif measure == 'week':
        row = 'total_average_weekly'
    elif measure == 'month':
        row = 'total_average_monthly'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('apple_article_results')
    table.update_item(
        Key={
            'sector': 'apple',
        },
        UpdateExpression='SET :val1 = :val2',
        ExpressionAttributeValues={
            ':val1': row
            ':val2': int(updated_prediction)
        }
    )

def get_highest_freq(classifications):
    return np.bincount(classifications).argmax()
