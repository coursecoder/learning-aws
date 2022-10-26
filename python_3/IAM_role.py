import boto3, json

def create_iam_role():
   
    iam = boto3.client("iam")

    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
                }
        ]                                               
    })
    
    # Define IAM role creation
    response = iam.create_role(
        RoleName = "Playdough-LambdaAccessToDynamoDB",
        AssumeRolePolicyDocument = assume_role_policy_document
    )
  
    return response["Role"]["RoleName"], response["Role"]["Arn"]

def create_iam_policy():
    iam = boto3.client('iam')

    # Define IAM policy to allow DynamoDB read-only access to Lambda
    my_managed_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "application-autoscaling:DescribeScalableTargets",
                    "application-autoscaling:DescribeScalingActivities",
                    "application-autoscaling:DescribeScalingPolicies",
                    "cloudwatch:DescribeAlarmHistory",
                    "cloudwatch:DescribeAlarms",
                    "cloudwatch:DescribeAlarmsForMetric",
                    "cloudwatch:GetMetricStatistics",
                    "cloudwatch:ListMetrics",
                    "cloudwatch:GetMetricData",
                    "datapipeline:DescribeObjects",
                    "datapipeline:DescribePipelines",
                    "datapipeline:GetPipelineDefinition",
                    "datapipeline:ListPipelines",
                    "datapipeline:QueryObjects",
                    "dynamodb:BatchGetItem",
                    "dynamodb:Describe*",
                    "dynamodb:List*",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:PartiQLSelect",
                    "dax:Describe*",
                    "dax:List*",
                    "dax:GetItem",
                    "dax:BatchGetItem",
                    "dax:Query",
                    "dax:Scan",
                    "ec2:DescribeVpcs",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeSecurityGroups",
                    "iam:GetRole",
                    "iam:ListRoles",
                    "kms:DescribeKey",
                    "kms:ListAliases",
                    "sns:ListSubscriptionsByTopic",
                    "sns:ListTopics",
                    "lambda:ListFunctions",
                    "lambda:ListEventSourceMappings",
                    "lambda:GetFunctionConfiguration",
                    "resource-groups:ListGroups",
                    "resource-groups:ListGroupResources",
                    "resource-groups:GetGroup",
                    "resource-groups:GetGroupQuery",
                    "tag:GetResources",
                    "kinesis:ListStreams",
                    "kinesis:DescribeStream",
                    "kinesis:DescribeStreamSummary"
                ],
                "Effect": "Allow",
                "Resource": "*"
            },
            {
                "Action": "cloudwatch:GetInsightRuleReport",
                "Effect": "Allow",
                "Resource": "arn:aws:cloudwatch:*:*:insight-rule/DynamoDBContributorInsights*"
            }
           
        ]
    }
    response = iam.create_policy(
        PolicyName='Playdough-LambdaAccessToDynamoDBPolicy',
        PolicyDocument=json.dumps(my_managed_policy)
    )
    return response["Policy"]["Arn"]

def attach_iam_policy(policy_arn, role_name):
    # Attach the policy to the role
    iam = boto3.client("iam")

    response = iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )

