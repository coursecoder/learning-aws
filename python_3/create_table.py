import boto3
import time

def create_table():

    DDB = boto3.resource('dynamodb', region_name='us-east-1')

    params = {
        'TableName': 'LeaderBoard',
        'KeySchema': [
            {'AttributeName': 'gamer_name', 'KeyType': 'HASH'},
            {'AttributeName': 'score', 'KeyType': 'RANGE'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'gamer_name', 'AttributeType': 'S'},
             {'AttributeName': 'score', 'AttributeType': 'N'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = DDB.create_table(**params)
    table.wait_until_exists()
    print ("Done")
    

if __name__ == '__main__':
    print("Creating DynamoDB table...this might take a minute...")
    create_table()


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
