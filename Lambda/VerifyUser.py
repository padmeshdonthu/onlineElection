import json

import boto3


def lambda_handler(event, context):
    json_data = json.loads(event["body"])

    email_id = json_data['email_id']
    verified = json_data['verified']

    dynamodb = boto3.resource("dynamodb")

    user_table = dynamodb.Table("user")

    response = user_table.update_item(
        Key={
            'email_id': email_id
        },
        UpdateExpression="set verified=:a",
        ExpressionAttributeValues={
            ':a': verified
        },
        ReturnValues="UPDATED_NEW"
    )

    response = {'email': email_id, 'verified': verified}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
