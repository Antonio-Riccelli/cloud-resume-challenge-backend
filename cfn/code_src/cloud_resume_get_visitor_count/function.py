import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: ")
    logger.info(json.dumps(event))

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])
    project_key = os.environ['DYNAMODB_PROJECT_KEY']
    
    response = table.get_item(
        Key={
            'project': project_key
        }
        )
    item = response['Item']
    visitors_count = item['visitors']
    print("visitors count", visitors_count)
    return {
        'statusCode': 200,
        'body': {
            'count': visitors_count
        }
    }
