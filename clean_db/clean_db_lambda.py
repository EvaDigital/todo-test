import boto3
from botocore.exceptions import ClientError
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('completed').eq(True)
        )

        items = response.get('Items', [])

        for item in items:
            todo_id = item.get('id')
            try:
                table.delete_item(
                    Key={
                        'id': todo_id
                    }
                )
                print(f"Deleted task with id: {todo_id}")
            except ClientError as ce:
                print(f"Error deleting task with id {todo_id}: {ce}")

        return {
            'statusCode': 200,
            'body': 'Success'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}'
        }

    