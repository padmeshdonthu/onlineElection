import json

import boto3


def lambda_handler(event, context):
    json_data = json.loads(event["body"])
    email_id = json_data['email_id']
    election_id = json_data['election_id']
    status = json_data['status']
    vote_date = json_data['vote_date']
    candidate_voted = json_data['candidate_voted']

    vote_details = {
        "voter_id": email_id,
        "election_id": election_id,
        "status": status,
        "vote_date": vote_date,
        "candidate_voted": candidate_voted
    }

    print(vote_details)
    client = boto3.resource("dynamodb")
    table = client.Table("election_voter_link")

    response = table.put_item(Item=vote_details)

    response = {'email': email_id}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
