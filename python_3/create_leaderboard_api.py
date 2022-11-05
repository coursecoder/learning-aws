import boto3, json
import time

region_name = 'us-east-1'
function_name = 'get_all_leaderboard'

client = boto3.client('apigateway', region_name)
lambda_client = boto3.client('lambda', region_name)

# create LeaderboardAPI
print("Creating API Gateway...")
time.sleep(2.4)
response = client.create_rest_api(
    name='LeaderboardApi',
    description='API to get leaderboard data',
    minimumCompressionSize=123,
    endpointConfiguration={
        'types': [
            'REGIONAL',
        ]
    }
)
api_id = response["id"]

# explicitly grant permission for APIGateway to invoke the Lambda function
lambda_client.add_permission(
    FunctionName=function_name, 
    # to make this Sid unique add the api_id number
    StatementId=f'api_invoke_lambda{api_id}', 
    Action='lambda:InvokeFunction', 
    Principal='apigateway.amazonaws.com' 
)

# get the root resource id
resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# create REST Endpoint of /leaderboard
print("Creating /leaderboard API endpoint...")
time.sleep(2.4)
leaderboard = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='leaderboard'
)
leaderboard_resource_id = leaderboard["id"]

# create an API method request of GET /leaderboard
leaderboard_method = client.put_method(
    restApiId=api_id,
    resourceId=leaderboard_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# set up the 200 OK response to the method request of GET /leaderboard
leaderboard_response = client.put_method_response(
    restApiId=api_id,
    resourceId=leaderboard_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        # these parameters allow Cross-Origin Resource Sharing (CORS) between S3 and APIGateway
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)

# lookup the Lambda function ARN
lambda_response = lambda_client.get_function(
    FunctionName=function_name)
lambda_arn = lambda_response["Configuration"]["FunctionArn"]

# set up the integration of the GET /leaderboard method with a Lambda function
leaderboard_integration = client.put_integration(
    restApiId=api_id,
    resourceId=leaderboard_resource_id,
    httpMethod='GET', # the method to use when calling the API Gateway endpoint
    integrationHttpMethod="POST", # the method used by API Gateway to call the backend - always POST for Lambda
    type='AWS', # type AWS for Lambda integration
    uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)

# get account id of the current aws user
account_id = boto3.client('sts').get_caller_identity().get('Account')

# add permission for API to trigger Lambda function
permission_response = lambda_client.add_permission(
    FunctionName=function_name,
    StatementId='playdough-apigateway-get1',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f"arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/GET/leaderboard"
)

leaderboard_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=leaderboard_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Methods': "'GET'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)

print("DONE")

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
