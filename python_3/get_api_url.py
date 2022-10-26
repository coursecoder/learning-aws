#import boto3, json
import time
import subprocess

region_name = 'us-east-1'
function_name = 'get_all_leaderboard'

#client = boto3.client('apigateway', region_name)

# get the api id for the LeaderboardApi
api_id = subprocess.getoutput("aws apigateway get-rest-apis --query 'items[?name==`LeaderboardApi`].[id]' --output text")
stage = 'prod'

def get_api_url():
        """
        Builds the REST API URL from its parts.

        """
        url = (f'https://{api_id}.execute-api.{region_name}.amazonaws.com/{stage}')
        return url

if __name__ == '__main__':
    api_url = get_api_url()
    print(api_url)