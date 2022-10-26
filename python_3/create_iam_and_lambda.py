import boto3
import subprocess
import IAM_role
import time


def create_iam():
    # create IAM role
    print("Creating IAM role...")
    role_data = IAM_role.create_iam_role()
    time.sleep(2.4)
    role_name = role_data[0]
    role_arn = role_data[1]
    print("IAM Role: " + role_name)
    print("IAM Role ARN: " + role_arn)

    # create IAM policy
    print("Creating IAM policy...")
    policy_arn = IAM_role.create_iam_policy()
    time.sleep(2.4)
    print("Policy ARN: " + policy_arn)

    # attach IAM policy to role
    print("Attaching IAM Policy to Role...")
    IAM_role.attach_iam_policy(policy_arn, role_name)
    time.sleep(3.4)

    return role_arn



def create_lambda(role_arn):
    # create lambda
    client = boto3.client('lambda', region_name='us-east-1')
    BUCKET = subprocess.getoutput('aws s3api list-buckets --query "Buckets[].Name" | grep -oh "\w*-leaderboard\w*" | xargs')
    print("Checking for Lambda code in: " + BUCKET)
    
    print("Creating Lambda function...")
    response = client.create_function(
        FunctionName='get_all_leaderboard',
        Runtime='python3.8',
        Role=role_arn,
        Handler='get_all_leaderboard_code.lambda_handler',
        Code={
            'S3Bucket': BUCKET,
            'S3Key': 'get_all_leaderboard_code.zip'
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
    role_arn = create_iam()
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
