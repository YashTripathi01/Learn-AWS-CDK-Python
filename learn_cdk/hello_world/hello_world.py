import json


def lambda_handler(event, context):
    body = {
        "message": "Hello, World!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

    return response
