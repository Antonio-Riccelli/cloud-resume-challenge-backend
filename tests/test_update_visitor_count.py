import unittest
from moto import mock_dynamodb2
import boto3
import os
target = __import__('../cfn/lambda_src/cloud-resume-update-visitor-count/lambda_function.py')
lambda_handler = target.lambda_handler

@mock_dynamodb2
class TestUpdateVisitorCount(unittest.TestCase):
    def test_update_visitor_count_successfully(self):
        """
        Create database resource and mock table
        """
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        table = dynamodb.create_table(
            TableName='cloud-resume-visitor-counter',
            KeySchema=[
                {'AttributeName': 'project', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {"AttributeName": "project", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()

        # Mock environmental variables
        os.environ['DYNAMODB_TABLE_NAME'] = table['TableDescription']['TableName']

        # Invoke lambda function
        event = {}
        result = lambda_handler(event, None)

        # Retrieve item from the table
        response = table.get_item(Key={'project': 'cloud-resume-challenge'})
        item = response.get('Item')

        # Assertions
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)
        self.assertEqual(result['body'], f'Visitor counter updated. Current count: {result["count"]}')
        self.assertEqual(result['count'], 1)

if __name__ == '__main__':
    unittest.main()