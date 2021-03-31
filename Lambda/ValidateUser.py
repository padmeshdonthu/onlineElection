import json, boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    json_data = json.loads(event["body"])
    email = json_data["email_id"]
    password = json_data["password"]
    client = boto3.resource("dynamodb")
    table = client.Table("user")
    
    response = table.get_item(
        Key={
            'email_id': email
        })
    
    json_body = {}
        
    if "Item" in response:
        json_body = response["Item"]
    
    responseObject = {}
    if json_body!= {} and email == json_body['email_id'] and password == json_body['password']:
        if json_body['verified'] == 'Y' :
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps(json_body)
        else:
            responseObject['statusCode'] = 404
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = "Email not verified"
    else:
        responseObject['statusCode'] = 404
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = "Invalid email_id"

    return responseObject