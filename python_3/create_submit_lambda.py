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
        FunctionName='submit_score',
        Runtime='python3.8',
        Role=role_arn,
        Handler='submit_score_code.lambda_handler',
        Code={
            'S3Bucket': BUCKET,
            'S3Key': 'submit_score_code.zip'
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
    



"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
