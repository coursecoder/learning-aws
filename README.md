## Introduction
The purpose of this work is to develop and deploy a leaderboard for your game using the following AWS resources: S3, APIGateway, Lambda, IAM, and DynamoDB. The choice of a highly available, scalable, and secure serverless environment with massive economies of scale will have several benefits to the end user, including:
- low product pricing
- fast response time, and
- reliable uptime

## Leaderboard Architecture
![AWS Architecture](https://github.com/coursecoder/learning-aws/blob/media/Playdough-AWS-Architecture.png)

## Project Organization
- **python_3 Folder:** This folder contains all python scripts that are used to build AWS infrastructure on the backend.
- **resources Folder:** This folder contains the initial setup script as well as the infrastructure for the frontend. 
    - **website Folder:** This folder contains all the images and code necessary to build a functional game with leaderboard.

## Requirements
- **AWS CLI:** See the [Getting started guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) in the *AWS CLI User Guide* for more information.
- **AWS Credentials:** Your AWS credentials need to have administrative privileges to IAM, S3, Lambda, API Gateway and DynamoDB. If you haven’t setup AWS credentials before, [this resource from AWS](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html) is helpful.
- **AWS SDK for Python:** You will need to be running the latest Boto3 release. See the [Boto3 Quickstart](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) for more information.

## Installation Instructions
### Step 1: Download project files
<pre><code>wget <path-to-code-on-github>
</code></pre>
### Step 2: Unzip project files
<pre><code>unzip code.zip
</code></pre>
### Step 3: Run setup script
- Set permissions on the script so that you can run it, and then run it:
<pre><code>chmod +x ./resources/setup.sh && ./resources/setup.sh
</code></pre>
- You will be asked to name your S3 bucket. Your bucket name must be appended with **-leaderboard** for the script to work. If you are not familiar with naming S3 buckets, see [Bucket Naming Rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).

The setup script creates the following resources:
1. An S3 bucket with an associated bucket policy. The bucket contains the game website code.
2. An Amazon DynamoDB table populated with leaderboard data.
The leaderboard is already pre-seeded with 25 users (json file is resources/website/all_gamers.json). The leaderboard avatars were generated using the 3rd party API [DiceBear Avatars](https://avatars.dicebear.com/).
3. A REST API configured using Amazon API Gateway.
    - All game data is exposed at /leaderboard (GET)
    - Data for the top six players is exposed at /leaderboard/top_players (GET)
    - Score submission endpoint is exposed at /score/submit (POST).
4. A Lambda function that retrieves data from DynamoDB when invoked. There is a policy that gives the Lambda function access to DynamoDB.