import boto3, json, time
import subprocess

region_name = 'us-east-1'
function_name = 'get_top_gamers'
api_name = 'LeaderboardApi'

client = boto3.client('apigateway', region_name)
lambda_client = boto3.client('lambda', region_name)

# get the api id for the LeaderboardApi
api_id = subprocess.getoutput("aws apigateway get-rest-apis --query 'items[?name==`LeaderboardApi`].[id]' --output text")

# lookup id for /leaderboard resource
response = client.get_resources(
    restApiId=api_id
)

# this doesn't always get the parent id
parent_id = response["items"][0]["id"]

# create /leaderboard/top_gamer endpoint
print("Creating /leaderboard/top_gamer API endpoint...")
time.sleep(2.4)
top_gamer = client.create_resource(
    restApiId=api_id,
    parentId=parent_id,
    pathPart='top_gamer'
)

top_gamer_resource_id = top_gamer["id"]

# create GET method for /leaderboard/top_gamer
top_gamer_method = client.put_method(
    restApiId=api_id,
    resourceId=top_gamer_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

top_gamer_response = client.put_method_response(
    restApiId=api_id,
    resourceId=top_gamer_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
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

# set up the integration of the GET /leaderboard/top_gamer method with a Lambda function
top_gamer_integration = client.put_integration(
    restApiId=api_id,
    resourceId=top_gamer_resource_id,
    httpMethod='GET', # the method to use when calling the API Gateway endpoint
    integrationHttpMethod="POST", # the method used by API Gateway to call the backend - always POST for Lambda
    type='AWS', # type AWS for Lambda integration
    uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
    requestTemplates={
        'application/json': '{"statusCode": 200}'
        # need to add this as mapping template?
        #{
        # "path": "$context.resourcePath"
        #}
    }
)

# get account id of the current aws user
account_id = boto3.client('sts').get_caller_identity().get('Account')

# add permission for API to trigger Lambda function
permission_response = lambda_client.add_permission(
    FunctionName=function_name,
    StatementId='playdough-apigateway-get2',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f"arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/GET/leaderboard/top_gamer"
) 

top_gamer_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=top_gamer_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Methods': "'GET'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)



print ("DONE")