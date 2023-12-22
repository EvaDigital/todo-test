import boto3
import json 
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
            }
    return wrapper


@exceptions
def list_todos():
    response = table.scan()
    todos = response.get('Items', [])

    return {
        'statusCode': 200,
        'body': json.dumps({'message': todos})
    }


@exceptions
def create_todo(event):
    todo_data = json.loads(event['body'])
        
    todo_id = str(uuid.uuid4())

    table.put_item(
        Item={
            'id': todo_id,
            'title': todo_data.get('title', ''),
            'description': todo_data.get('description', ''),
            'completed': False 
        }
    )

    return {
        'statusCode': 201,
        'body': json.dumps({'message': {'id': todo_id}})
    }
    

@exceptions
def get_todo(todo_id):
    response = table.get_item(
        Key={
            'id': todo_id
        }
    )
    todo = response.get('Item')

    if todo:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': todo})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Todo not found'})
        }
    

@exceptions
def update_todo(todo_id, event):
    updated_todo_data = json.loads(event['body'])

    update_expression = 'SET ' + ', '.join([f'{key} = :{key}' for key, value in updated_todo_data.items() if value is not None and value != ''])
    expression_attribute_values = {f':{key}': value for key, value in updated_todo_data.items() if value is not None and value != ''}

    table.update_item(
        Key={
            'id': todo_id
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Todo updated successfully'})
    }


@exceptions
def delete_todo(todo_id):
    table.delete_item(
        Key={
            'id': todo_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Todo deleted successfully'})
    }