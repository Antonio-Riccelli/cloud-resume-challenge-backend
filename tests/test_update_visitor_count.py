import unittest
from unittest.mock import patch
from moto import mock_dynamodb
import boto3
import os
from cfn.code_src.cloud_resume_update_visitor_count.function import lambda_handler

@mock_dynamodb
class TestUpdateVisitorCount(unittest.TestCase):
    def setUp(self):
        """
        Start the moto DynamoDB mock
        """
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table_name = 'cloud-resume-visitor-counter'
        self.table = self.dynamodb.create_table(
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
        self.table.wait_until_exists()

        # Set environmental variables
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['DYNAMODB_TABLE_NAME'] = self.table_name

    def test_lambda_handler(self):        
        # Mock DynamoDB Table resource
        table_mock = self.dynamodb.Table(self.table_name)

        # Set up initial item in table
        table_mock.put_item(Item={'project': 'cloud-resume-challenge', 'visitors': 0})

        # Patch the boto3.resource and table.get_item calls in the lambda function
        with patch('boto3.resource') as resource_mock, patch.object(table_mock, 'get_item') as get_item_mock, patch.object(table_mock, 'update_item') as update_item_mock:
            # Set return values of mocks
            resource_mock.return_value = self.dynamodb
            get_item_mock.return_value = {
                'Item': {
                    'visitors' : 0 # Mock current value of visitors
                }
            }

            # Call lambda handler with sample event
            event = {}
            response = lambda_handler(event, None)

        # Assert that the expected DynamoDB methods were called
        # get_item_mock.assert_called_with(
        #     TableName=self.table_name,
        #     Key={'project': 'cloud-resume-challenge'},
        #     ProjectionExpression='visitors'
        # )
        # update_item_mock.assert_called_with(
        #     TableName=self.table_name,
        #     Key={'project': 'cloud-resume-challenge'},
        #     UpdateExpression='SET visitors = :start + :incr',
        #     ExpressionAttributeValues={':start': 5, ':incr': 1},
        #     ReturnValues='UPDATED_NEW'
        # )

        # Assert response from the lambda function
        expected_response = {
            'statusCode': 200,
            'body': f'Visitor counter updated. Current count: 1',
            'count': 1 # Mock current value of visitors'
        }
        self.assertEqual(response, expected_response)
    
    def tearDown(self):
        # Stop mock dynamodb
        self.table.delete()

if __name__ == '__main__':
    unittest.main()
