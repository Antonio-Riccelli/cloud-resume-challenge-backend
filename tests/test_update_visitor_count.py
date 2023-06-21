import unittest
from moto import mock_dynamodb
import boto3
import os
from cfn.code_src.cloud_resume_update_visitor_count.function import lambda_handler

@mock_dynamodb
class TestUpdateVisitorCount(unittest.TestCase):
    def test_update_visitor_count_successfully(self):
        """
        Create database resource and mock table
        """
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        print("Creating table...")
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
        print("table", table)
        print("Mocking env variables...")
        os.environ['DYNAMODB_TABLE_NAME'] = "cloud-resume-visitor-counter"
        os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
        print("Default region", os.environ['AWS_DEFAULT_REGION'])

        # Invoke lambda function
        print("Invoking lambda function...")
        event = {}
        result = lambda_handler(event, None)

        print("retrieving item from table...")
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