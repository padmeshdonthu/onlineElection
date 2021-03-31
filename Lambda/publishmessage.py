import json
import boto3

def lambda_handler(event, context):
    json_data = json.loads(event["body"])
    email = json_data["email_id"]
    message = json_data["message"]
    for id in email:
        e_value = id.split('@')[0]
        responseObject = {}
        session = boto3.session.Session()
        client = session.client(
            service_name='sns',
            region_name='us-east-1'
        )
        topic_arn = "arn:aws:sns:us-east-1:629166367933:CastVoteNotification"+ e_value
        response = client.publish(
            Message=message,
            TopicArn=topic_arn
        )
        responseObject ={}
        response = True
        if response:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = "Published the message to the user"
        else:
            responseObject['statusCode'] = 404
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = "Some error has occurred and the message is not published"
    return responseObject