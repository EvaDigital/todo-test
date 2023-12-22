from api import list_todos, create_todo, get_todo, update_todo, delete_todo


def lambda_handler(event, context):
    path = event.get('path', '/')

    if path == '/todo/list' and event['httpMethod'] == 'GET':
        return list_todos()

    elif path == '/todo/create' and event['httpMethod'] == 'POST':
        return create_todo(event)

    elif path.startswith('/todo/') and event['httpMethod'] == 'GET':
        todo_id = path.split('/')[-1]
        return get_todo(todo_id)

    elif path.startswith('/todo/update/') and event['httpMethod'] == 'PUT':
        todo_id = path.split('/')[-1]
        return update_todo(todo_id, event)

    elif path.startswith('/todo/delete/') and event['httpMethod'] == 'DELETE':
        todo_id = path.split('/')[-1]
        return delete_todo(todo_id)

    return {
        'statusCode': 404,
        'body': 'Not Found'
    }
