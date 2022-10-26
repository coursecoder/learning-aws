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

leaderboard_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=leaderboard_resource_id,
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
		},
		{
			"gamer_name_str": "vanilla glazed doughnut",
			"gamer_id_str": "a453",
			"score_int": 999,
			"rank_int": 7,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "boston cream doughnut",
			"gamer_id_str": "a458",
			"score_int": 997,
			"rank_int": 8,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "bernadine",
			"gamer_id_str": "a450",
			"score_int": 995,
			"rank_int": 9,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "peanutbutter and chocolate cupcake",
			"gamer_id_str": "a451",
			"score_int": 990,
			"rank_int": 10,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "poppy seed bagel",
			"gamer_id_str": "a466",
			"score_int": 985,
			"rank_int": 11,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "cinnamon doughnut",
			"gamer_id_str": "a454",
			"score_int": 980,
			"rank_int": 12,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "lemon pie",
			"gamer_id_str": "a461",
			"score_int": 970,
			"rank_int": 13,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "chocolate iced doughnut",
			"gamer_id_str": "a464",
			"score_int": 962,
			"rank_int": 14,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "garlic bagel",
			"gamer_id_str": "a467",
			"score_int": 955,
			"rank_int": 15,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "chocolate cake slice",
			"gamer_id_str": "a445",
			"score_int": 950,
			"rank_int": 16,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "blueberry bagel",
			"gamer_id_str": "a467",
			"score_int": 874,
			"rank_int": 17,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "chocolate cake",
			"gamer_id_str": "a446",
			"score_int": 715,
			"rank_int": 18,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "powdered sugar doughnut",
			"gamer_id_str": "a456",
			"score_int": 603,
			"rank_int": 19,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "chocolate doughnut",
			"gamer_id_str": "a455",
			"score_int": 502,
			"rank_int": 20,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "lemon pie slice",
			"gamer_id_str": "a460",
			"score_int": 494,
			"rank_int": 21,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "cherry pie slice",
			"gamer_id_str": "a462",
			"score_int": 395,
			"rank_int": 22,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "eclair",
			"gamer_id_str": "a459",
			"score_int": 200,
			"rank_int": 23,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "vanilla cupcake",
			"gamer_id_str": "a449",
			"score_int": 150,
			"rank_int": 24,
			"tag_str_arr": [
				"not registered"
			]
		},
		{
			"gamer_name_str": "raspberry jelly doughnut",
			"gamer_id_str": "a457",
			"score_int": 101,
			"rank_int": 25,
			"tag_str_arr": [
				"not registered"
			]
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
