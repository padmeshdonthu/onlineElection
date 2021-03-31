import json

import boto3


def lambda_handler(event, context):
    json_data = json.loads(event["body"])

    ename = json_data['ename']
    startDate = json_data['startDate']
    candidates = json_data['candidates']

    election_details = {
        "ename": ename,
        "startDate": startDate,
        "candidates": candidates
    }

    print(election_details)
    client = boto3.resource("dynamodb")
    table = client.Table("election")

    response = table.put_item(Item=election_details)

    response = {'ename': ename}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
