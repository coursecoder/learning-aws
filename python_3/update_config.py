
import boto3
import subprocess
import time

S3API = boto3.client("s3", region_name="us-east-1") 
bucket_name = subprocess.getoutput('aws s3api list-buckets --query "Buckets[].Name" | grep -oh "\w*-leaderboard\w*" | xargs')
    

filename = "./resources/website/config.js"

# uploading config.js file with frontend variables to S3 bucket
print("Updating Website Config...")
time.sleep(2.4)
S3API.upload_file(filename, bucket_name, "config.js", ExtraArgs={'ContentType': "application/js", "CacheControl": "max-age=0"})


print ("DONE")
