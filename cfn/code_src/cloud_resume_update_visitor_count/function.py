import boto3
import os

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', os.environ['AWS_DEFAULT_REGION'])
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

    current_value_response = table.get_item(
        TableName = os.environ['DYNAMODB_TABLE_NAME'],
        Key={
            'project':'cloud-resume-challenge'
        },
        ProjectionExpression='visitors'
        )
    
    current_value = current_value_response['Item']['visitors']
    print("Visitors counter, current value:", current_value)

    response = table.update_item(
        TableName = os.environ['DYNAMODB_TABLE_NAME'],
        Key={
            'project': 'cloud-resume-challenge'
        },
        UpdateExpression= 'SET visitors = :start + :incr',
        ExpressionAttributeValues={
            ':start': current_value or 0,
            ':incr': 1
        },
        ReturnValues='UPDATED_NEW'
        )
   
    counter_value = response['Attributes']['visitors']
    print(f'Visitor counter updated. Current count: {counter_value}')
    return {
        'statusCode': 200,
        'body': f'Visitor counter updated. Current count: {counter_value}',
        'count': f'{counter_value}'
    }