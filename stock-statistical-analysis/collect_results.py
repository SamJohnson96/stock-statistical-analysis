import imp
import json
import sys
import time
from datetime import datetime

def lambda_handler(event, context):
    print(record)
    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            article_content = record['dynamodb']['NewImage']['article_content']['S']
            article_id = record['dynamodb']['NewImage']['article_id']['N']
        else:
            print('No article to scrape')
            return;

# Insert row into Dynamodb table processed_articles
# def insert_row(article_id,article_content,classification):
#     print('--- inserting row ---')
#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table('results')
#     table.put_item(
#         Item={
#             'article_id' :  int(article_id),
#             'naive_bayes_classification' : str(classification, 'utf-8')
#         }
#     )
