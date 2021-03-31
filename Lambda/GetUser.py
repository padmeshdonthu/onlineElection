import json, boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    email = event["queryStringParameters"]["email_id"]
    client = boto3.resource("dynamodb")
    table = client.Table("user")

    response = table.get_item(
        Key={
            'email_id': email
        })

    if "Item" in response:
        json_body = response["Item"]
    else:
        json_body = {}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(json_body)

    return responseObject