import boto3, json
import time
import subprocess

region_name = 'us-east-1'
function_name = 'submit_score'

client = boto3.client('apigateway', region_name)
lambda_client = boto3.client('lambda', region_name)

api_id = subprocess.getoutput("aws apigateway get-rest-apis --query 'items[?name==`LeaderboardApi`].[id]' --output text")

# get the root resource id
resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# create REST Endpoint of /submit_score
print("Creating /score/submit API endpoint...")
score = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='score'
)
time.sleep(2.4)
score_id = score["id"]


# create /score/submit endpoint

time.sleep(2.4)
submit = client.create_resource(
    restApiId=api_id,
    parentId=score_id,
    pathPart='submit'
)

submit_id = submit["id"]

# create an API method request of POST /submit
submit_method = client.put_method(
    restApiId=api_id,
    resourceId=submit_id,
    httpMethod='POST',
    authorizationType='NONE'
)


submit_response = client.put_method_response(
    restApiId=api_id,
    resourceId=submit_id,
    httpMethod='POST',
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

# set up the integration of the POST /score/submit method with a Lambda function
submit_integration = client.put_integration(
    restApiId=api_id,
    resourceId=submit_id,
    httpMethod='POST',
    integrationHttpMethod="POST",
    type='AWS',
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
    StatementId='playdough-apigateway-get',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f"arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/POST/score/submit"
)

submit_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=submit_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'*'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
    #responseTemplates={
        #"application/json": json.dumps({
            #"message" : "Your score was submitted successfully!"
        #"gamer_name" : "$input.params('gamer_name')",
        #"gamer_score" : "$input.params('gamer_score')"
       # })
    #}
)

# deploy API to prod
deployment_response = client.create_deployment(
    restApiId=api_id,
    stageName='prod',
)

print ("DONE")

