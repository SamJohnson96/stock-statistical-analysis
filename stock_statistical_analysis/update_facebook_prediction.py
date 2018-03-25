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
    table = dynamodb.Table('facebook_article_results')
    pk_key = 'article_id'

    # Get row
    response = table.get_item(Key={pk_key: int(article_id)})
    article = response['Item']

    if 'naive_bayes' in article.keys() and 'support_vector_machine' in article.keys() and 'extra_trees' in article.keys() and 'k_nearest' in article.keys() and 'linear_perceptron' in article.keys():
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
    table = dynamodb.Table('facebook_article_results')

    article_id = article['article_id']
    hour_ago = article_id - 3600

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(hour_ago),int(article_id))
                )

    # Get classifications
    svm_classification = article['support_vector_machine']
    naive_bayes_classification = article['naive_bayes']
    extra_trees_classification = article['extra_trees']
    k_nearest_classification = article['k_nearest']
    linear_perceptron_classification = article['linear_perceptron']

    # Update all fields in table
    update_svm_classification('hour',response,svm_classification)
    update_naive_bayes_classification('hour',response,naive_bayes_classification)
    update_extra_trees_classification('hour',response,extra_trees_classification)
    update_linear_perceptron_classification('hour',response,linear_perceptron_classification)
    update_k_neighbors_classification('hour',response,k_nearest_classification)
    update_average('hour',response, naive_bayes_classification, svm_classification, extra_trees_classification, k_nearest_classification, linear_perceptron_classification)
    mark_as_changed('hour')

def update_day(article):
    print('--- Updating day ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('facebook_article_results')

    article_id = article['article_id']
    twenty_four_hours_ago = article_id - (24*3600)

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(twenty_four_hours_ago),int(article_id))
             )

    # Get classifications
    svm_classification = article['support_vector_machine']
    naive_bayes_classification = article['naive_bayes']
    extra_trees_classification = article['extra_trees']
    k_nearest_classification = article['k_nearest']
    linear_perceptron_classification = article['linear_perceptron']

    # Update all fields in table
    update_svm_classification('day',response,svm_classification)
    update_naive_bayes_classification('day',response,naive_bayes_classification)
    update_extra_trees_classification('day',response,extra_trees_classification)
    update_linear_perceptron_classification('day',response,linear_perceptron_classification)
    update_k_neighbors_classification('day',response,k_nearest_classification)
    update_average('day',response, naive_bayes_classification, svm_classification, extra_trees_classification, k_nearest_classification, linear_perceptron_classification)
    mark_as_changed('day')

def update_week(article):
    print('--- Updating week ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('facebook_article_results')

    article_id = article['article_id']
    a_week_ago = article_id - (7*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(a_week_ago),int(article_id))
             )

    # Get classifications
    svm_classification = article['support_vector_machine']
    naive_bayes_classification = article['naive_bayes']
    extra_trees_classification = article['extra_trees']
    k_nearest_classification = article['k_nearest']
    linear_perceptron_classification = article['linear_perceptron']

    # Update all fields in table
    update_svm_classification('week',response,svm_classification)
    update_naive_bayes_classification('week',response,naive_bayes_classification)
    update_extra_trees_classification('week',response,extra_trees_classification)
    update_linear_perceptron_classification('week',response,linear_perceptron_classification)
    update_k_neighbors_classification('week',response,k_nearest_classification)
    update_average('week',response, naive_bayes_classification, svm_classification, extra_trees_classification, k_nearest_classification, linear_perceptron_classification)
    mark_as_changed('week')

def update_month(article):
    print('--- Updating hour ---')
    # Configuration for database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('facebook_article_results')

    article_id = article['article_id']
    a_month_ago = article_id - (31*(24*3600))

    response = table.scan(
                        Select='ALL_ATTRIBUTES',
                        FilterExpression=Key('article_id').between(int(a_month_ago),int(article_id))
             )

    # Get classifications
    svm_classification = article['support_vector_machine']
    naive_bayes_classification = article['naive_bayes']
    extra_trees_classification = article['extra_trees']
    k_nearest_classification = article['k_nearest']
    linear_perceptron_classification = article['linear_perceptron']

    # Update all fields in table
    update_svm_classification('month',response,svm_classification)
    update_naive_bayes_classification('month',response,naive_bayes_classification)
    update_extra_trees_classification('month',response,extra_trees_classification)
    update_k_neighbors_classification('month',response,k_nearest_classification)
    update_linear_perceptron_classification('month',response,linear_perceptron_classification)
    update_average('month',response, naive_bayes_classification, svm_classification, extra_trees_classification, k_nearest_classification, linear_perceptron_classification)
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
                'sector': 'facebook',
            },
            UpdateExpression='SET support_vector_machine_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET support_vector_machine_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET support_vector_machine_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
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
                'sector': 'facebook',
            },
            UpdateExpression='SET naive_bayes_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET naive_bayes_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET naive_bayes_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET naive_bayes_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )


def update_linear_perceptron_classification(measure, results, new_classification):
    print('--- Updating Linear Perceptron for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    linear_perceptron_classification = []
    linear_perceptron_classification.append(new_classification)
    for result in results:
        linear_perceptron_classification.append(result['linear_perceptron'])
    updated_prediction = get_highest_freq(linear_perceptron_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET linear_perceptron_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET linear_perceptron_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET linear_perceptron_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET linear_perceptron_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )


def update_k_neighbors_classification(measure, results, new_classification):
    print('--- Updating K Nearest Neighbors for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    k_nearest_classification = []
    k_nearest_classification.append(new_classification)
    for result in results:
        k_nearest_classification.append(result['k_nearest'])
    updated_prediction = get_highest_freq(k_nearest_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET k_nearest_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET k_nearest_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET k_nearest_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET k_nearest_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )

def update_extra_trees_classification(measure, results, new_classification):
    print('--- Updating Extra Trees for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    extra_tree_classification = []
    extra_tree_classification.append(new_classification)
    for result in results:
        extra_tree_classification.append(result['extra_trees'])
    updated_prediction = get_highest_freq(extra_tree_classification)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET extra_trees_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET extra_trees_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET extra_trees_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET extra_trees_monthly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )

def update_average(measure, results, naive_bayes, svm_classification,extra_trees,k_nearest,linear_perceptron):
    print('--- Updating Total Average for %s ---' % measure)
    results = results['Items']
    #Go through each result and get svm classification row
    all_classification = []
    all_classification.append(naive_bayes)
    all_classification.append(svm_classification)
    all_classification.append(extra_trees)
    all_classification.append(k_nearest)
    all_classification.append(linear_perceptron)

    for result in results:
        all_classification.append(result['naive_bayes'])
        all_classification.append(result['support_vector_machine'])
        all_classification.append(result['extra_trees'])
        all_classification.append(result['k_nearest'])
        all_classification.append(result['linear_perceptron'])

    updated_prediction = get_highest_freq(all_classification)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if measure == 'hour':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET total_average_hourly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET total_average_daily = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET total_average_weekly = :val1',
            ExpressionAttributeValues={
                ':val1': int(updated_prediction)
            }
        )
    elif measure == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
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

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('predictions')

    if time_interval == 'hour':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET hour_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif time_interval =='day':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET day_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif time_interval == 'week':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET week_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
    elif time_interval == 'month':
        table.update_item(
            Key={
                'sector': 'facebook',
            },
            UpdateExpression='SET month_change = :val1',
            ExpressionAttributeValues={
                ':val1': 1
            }
        )
