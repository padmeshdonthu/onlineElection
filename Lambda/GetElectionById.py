import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    election_id = event["queryStringParameters"]["election_id"]
    client = boto3.resource("dynamodb")
    table = client.Table("electionInfo")

    response = table.get_item(
        Key={
            'election_id': election_id
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