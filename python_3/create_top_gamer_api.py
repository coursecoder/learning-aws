import boto3, json, time
import subprocess

region_name = 'us-east-1'
function_name = 'get_all_leaderboard'
api_name = 'LeaderboardApi'

client = boto3.client('apigateway', region_name)
lambda_client = boto3.client('lambda', region_name)

# get the api id for the LeaderboardApi
api_id = subprocess.getoutput("aws apigateway get-rest-apis --query 'items[?name==`LeaderboardApi`].[id]' --output text")

# lookup id for /leaderboard resource
response = client.get_resources(
    restApiId=api_id
)

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
    # need to add this as mapping template
    #{
    # "path": "$context.resourcePath"
    #}
    }
)

top_gamer_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=top_gamer_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseTemplates={
        "application/json": json.dumps({
	"leaderboard_item_arr": [
		{
			"gamer_name_str": "hooper",
			"gamer_id_str": "a448",
			"score_int": 3004,
			"rank_int": 1,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		},
		{
			"gamer_name_str": "mattie",
			"gamer_id_str": "a455",
			"score_int": 2468,
			"rank_int": 2,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		},
		{
			"gamer_name_str": "cunningham",
			"gamer_id_str": "a452",
			"score_int": 1201,
			"rank_int": 3,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		},
		{
			"gamer_name_str": "nixon",
			"gamer_id_str": "a444",
			"score_int": 1129,
			"rank_int": 4,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		},
		{
			"gamer_name_str": "miles",
			"gamer_id_str": "a463",
			"score_int": 1019,
			"rank_int": 5,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		},
		{
			"gamer_name_str": "parks",
			"gamer_id_str": "a465",
			"score_int": 1005,
			"rank_int": 6,
			"tag_str_arr": [
				"not registered",
				"top gamer"
			],
			"special_int": 1
		}
	]
})
    },
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Methods': "'GET'",
        'method.response.header.Access-Control-Allow-Origin': "'*'"
    }
)


# deploy API to prod
deployment_response = client.create_deployment(
    restApiId=api_id,
    stageName='prod',
)

print ("DONE")