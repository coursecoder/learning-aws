import boto3
import subprocess
import time



def lookupRole():
    client = boto3.client('iam')
    response = client.get_role(
        RoleName='Playdough-LambdaAccessToDynamoDB'
    )
    role_arn = response["Role"]["Arn"]
    print("IAM Role ARN: " + role_arn)

    return role_arn

def create_lambda(role_arn):
    # create lambda
    client = boto3.client('lambda', region_name='us-east-1')
    BUCKET = subprocess.getoutput('aws s3api list-buckets --query "Buckets[].Name" | grep -oh "\w*-leaderboard\w*" | xargs')
    
    print("Creating next Lambda function...")
    response = client.create_function(
        FunctionName='get_top_gamers',
        Runtime='python3.8',
        Role=role_arn,
        Handler='get_top_gamers_code.lambda_handler',
        Code={
            'S3Bucket': BUCKET,
            'S3Key': 'get_top_gamers_code.zip'
        }
    )
    time.sleep(4.4)
    # return the lambda uri
    lambda_arn = response["FunctionArn"]
    print("Lambda ARN: " + lambda_arn)
    # construct lambda uri
    lambda_uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
    print("Lambda URI: " + lambda_uri)
    # return lambda_uri

if __name__ == '__main__':
    role_arn = lookupRole()
    create_lambda(role_arn)