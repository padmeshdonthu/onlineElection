import boto3
import json


def lambda_handler(event, context):
    json_data = json.loads(event["body"])

    election_id = json_data['election_id']
    results_published = "Y"

    dynamodb = boto3.resource("dynamodb")

    electionInfo_table = dynamodb.Table("electionInfo")

    response = electionInfo_table.update_item(
        Key={
            'election_id': election_id
        },
        UpdateExpression="set results_published=:a",
        ExpressionAttributeValues={
            ':a': results_published
        },
        ReturnValues="UPDATED_NEW"
    )

    response = {'election_id': election_id, 'results_published': results_published}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
