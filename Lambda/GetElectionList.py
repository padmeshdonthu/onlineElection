import boto3
import json


def lambda_handler(event, context):
    email = event["queryStringParameters"]["email_id"]
    client = boto3.resource("dynamodb")
    table = client.Table("electionInfo")

    response = table.scan()

    if "Items" in response:
        json_body = response["Items"]
    else:
        json_body = {}

    electionInfo = {}
    electionInfo['elections'] = json_body

    table = client.Table("election_voter_link")
    response = table.scan()

    electionInfo["submittedElections"] = response.get('Items', [])

    print(electionInfo)

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(electionInfo)

    return responseObject
