import boto3
import json
import time


S3API = boto3.client("s3", region_name="us-east-1")
bucket_name = "playdough-leaderboard"
policy_file = open("./resources/s3_policy.json", "r")

#attach JSON policy to S3 bucket to only grant access to the IP address entered
print("Adding bucket policy...")
time.sleep(2.4)
S3API.put_bucket_policy(
    Bucket = bucket_name,
    Policy = policy_file.read()
)