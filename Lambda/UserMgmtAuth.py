import boto3
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    authToken = event['authorizationToken'] 
    
    secret_name = "usermgmt/usrmgmtkey"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secret = eval(secret)
            if 'UsermgmtAPIKey' in secret:
                response = validate_keys(authToken,secret['UsermgmtAPIKey'])
                return response
            
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

def validate_keys(authToken,secret_val):  
    
    status = "Deny"
    if authToken == secret_val:
        status = "Allow"
    else:
        status = "Deny"
    
    responseObject = {}
    responseObject = {
         "principalId": secret_val, 
         "policyDocument": 
             { 
                 "Version": "2012-10-17", 
                 "Statement": [
                     {
                         "Action": "execute-api:Invoke", 
                         "Resource": ["arn:aws:execute-api:us-east-1:629166367933:as5r1zw6c8/*/*/usermanagement","arn:aws:execute-api:us-east-1:629166367933:as5r1zw6c8/*/POST/login"], 
                         "Effect": status
                         
                     }
                     ] 
                 
             }

    }
    return responseObject
