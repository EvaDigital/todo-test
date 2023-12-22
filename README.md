# Deployment Guide

## 1. Clone the project

## 2. Install AWS CLI
macOS and Linux: Install AWS CLI using package management tools. For example, on macOS, you can use Homebrew:
```
$ brew install awscli
``` 
if you are a Windows platform, you need follow this link and install from [AWS Official Site](https://aws.amazon.com/ru/cli/)

## 3. Configuring AWS CLI
After installing AWS CLI, run:
```
$ aws configure
```

## 4. Installing AWS CDK
Install AWS CDK using package management tools:
```
$ npm install -g aws-cdk
```

## 5. Create a virtualenv
```
$ python3 -m venv env
```
After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .\env\Scripts\activate
```

## 6. Install dependencies
Once the virtualenv is activated, you can install the required dependencies:
```
$ pip install -r requirements.txt
```

## 7. Synthesize the CloudFormation
At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

## 8. Deploy the project
```
$ cdk deploy
```
Upon successful deployment, you will receive outputs, and among them, you'll find a link to your deployed application. For example:
```
Outputs:
TodoListApiStack.TodoApiEndpointC1E16B6C = https://5ja2dqcgk6.execute-api.eu-central-1.amazonaws.com/prod/
```

# API
### Base URL

All API requests should be made to:

```
TodoApiEndpointC1E16B6C + todo/
```

### `/todo/list` (GET)

Get todos list

#### Request
- Method: GET
- URL: `/todo/list`

#### Response
```json
{
    "message": [
        {
            "completed": false,
            "description": "create some action",
            "id": "8b2e11e5-08eb-4f5d-ae05-1d00b6c286ad",
            "title": "test task 3"
        }
    ]
}
```

### `/todo/create` (POST)

Create new task

#### Request
- Method: POST
- URL: `/todo/create`

body:
```json
{
    "title": "new title",
    "description": "new one"
}
```
#### Response
```json
{
    "message": {
        "id": "9ad2f2b6-fe31-463e-877c-69eeee5c0772"
    }
}
```

### `/todo/update/{id}` (PUT)

Update task data
You can update one field or all fields

- Method: PUT
- URL: `/todo/update/{id}`
body:
```json
{
    "title": "new title",
    "description": "new one",
    "completed": true
}
```
#### Response
```json
{
    "message": "Todo updated successfully"
}
```

### `/todo/delete/{id}` (DELETE)

Delete task
- Method: PUT
- URL: `/todo/delete/{id}`

#### Response
```json
{
    "message": "Todo deleted successfully"
}
```