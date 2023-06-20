import unittest
import moto
target = __import__('../cfn/lambda_src/cloud-resume-update-visitor-count/lambda_function.py')
lambda_handler = target.lambda_handler

class TestUpdateVisitorCount(unittest.TestCase):
    def test_update_visitor_count(self):
        """
        Test that the lambda function is able to update the visitor count.
        """
        event = {}
        expected = {
            'statusCode': 200
        }
        result = lambda_handler(event, None)
        self.assertEqual(expected['statusCode'], result['statusCode'])

if __name__ == '__main__':
    unittest.main()