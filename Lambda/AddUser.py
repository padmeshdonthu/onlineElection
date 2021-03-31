import json

import boto3

print("Loading function")


def lambda_handler(event, context):
    json_data = json.loads(event["body"])

    email_id = json_data['email_id']
    first_name = json_data['first_name']
    last_name = json_data['last_name']
    password = json_data['password']
    phone = json_data['phone']
    verified = json_data['verified']

    user_details = {
        "email_id": email_id,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "phone": phone,
        "verified": verified
    }

    print(user_details)
    client = boto3.resource("dynamodb")
    table = client.Table("user")

    response = table.put_item(Item=user_details)

    response = {'email': email_id}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
