import boto3
import json

from boto3.dynamodb.conditions import Attr


def lambda_handler(event, context):
    election_id = event["queryStringParameters"]["election_id"]
    client = boto3.resource("dynamodb")
    table = client.Table("election_voter_link")

    response = table.scan(FilterExpression=Attr("election_id").eq(election_id))

    if "Items" in response:
        json_body = response["Items"]
    else:
        json_body = {}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(json_body)

    return responseObject
