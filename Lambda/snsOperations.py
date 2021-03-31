import json
import boto3

def lambda_handler(event, context):
    json_data = json.loads(event["body"])
    email = json_data["email_id"]
    session = boto3.session.Session()
    client = session.client(
        service_name='sns',
        region_name='us-east-1'
    )
    topic_name = 'CastVoteNotification' + email.split('@')[0]
    response = client.create_topic(
    Name=topic_name
    )
    responseObject = {}
    if 'TopicArn' in response:
        print("created topic")
        topic_arn = response['TopicArn']
        print('topic_val')
        status = client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint= email
        )

        print(status)
        responseObject['statusCode'] = 200
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = "Topic is created and subscription mail is sent"

    else:
        responseObject['statusCode'] = 404
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = "Some error has occurred and the topic is not created"
    return responseObject
    
