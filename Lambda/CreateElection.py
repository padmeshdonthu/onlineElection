import json
import boto3


def lambda_handler(event, context):
    json_data = json.loads(event["body"])

    election_id = json_data['election_id']
    election_type = json_data['election_type']
    election_title = json_data['election_title']
    election_text = json_data['election_text']
    start_date = json_data['start_date']
    end_date = json_data['end_date']
    results_published = json_data['results_published']
    election_candidates = json_data['election_candidates']

    election_details = {
        "election_id": election_id,
        "election_type": election_type,
        "election_title": election_title,
        "election_text": election_text,
        "start_date": start_date,
        "end_date": end_date,
        "election_candidates": election_candidates,
        "results_published": results_published
    }

    print(election_details)
    client = boto3.resource("dynamodb")
    table = client.Table("electionInfo")

    response = table.put_item(Item=election_details)

    response = {'election_id': election_id}

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response)

    return responseObject
