import boto3, json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Key, Attr, Not

TABLE_NAME_STR = 'LeaderBoard'
INDEX_NAME_STR = 'special_GSI'
DDB = boto3.resource('dynamodb', region_name='us-east-1')
    
def lambda_handler(event, context):
   # if top_gamer path exists then scan table for top gamers
    topgamers_path_str = event.get('path')
    if topgamers_path_str is not None:
        return scan_index(event, context)
    else:
        pass
    print("Running scan on table...")
    
    DDB = boto3.resource('dynamodb', region_name='us-east-1')

    TABLE = DDB.Table(TABLE_NAME_STR)
    
    response = TABLE.scan()
    
    data = response['Items']
    

    
    while 'LastEvaluatedKey' in response:
        response = TABLE.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        print("We needed to paginate and extend the response")
        data.extend(response['Items'])
        
    #python returns non standard JSON
    #so we need to convert some data to integers
    for item in data:
        item['score_int'] = item.pop('score')
        if item.get('special') is not None:
            item['special_int'] = item.pop('special')
        item['tag_str_arr'] = item.pop('tags')
        item['rank_int'] = item.pop('rank')
        item['gamer_name_str'] = item.pop('gamer_name')
        item['gamer_id_str'] = item.pop('gamer_id')
       
        if item['score_int']:
            item['score_int'] = int(item['score_int'])
        if item['rank_int']:
            item['rank_int'] = int(item['rank_int'])
        if item.get('special_int') is not None:
            item['special_int'] = int(item['special_int'])

    return_me={"leaderboard_item_arr": data}
    
    return return_me
    
def scan_index(event, context):

    print("Running scan on index...")
    ## event and context not used
    TABLE = DDB.Table(TABLE_NAME_STR)

    
    response = TABLE.scan(
        IndexName=INDEX_NAME_STR,
        FilterExpression=Not(Attr("tags").contains("not registered"))
    )

    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = TABLE.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            IndexName=INDEX_NAME_STR,
            FilterExpression=Not(Attr("tags").contains("not registered"))
        )
        print("We needed to paginate and extend the response")
        data.extend(response['Items'])
        
    #python returns non standard JSON
    #so we need to convert some data to integers
    for item in data:
        item['score_int'] = item.pop('score')
        item['special_int'] = item.pop('special')
        item['tag_str_arr'] = item.pop('tags')
        item['rank_int'] = item.pop('rank')
        item['gamer_name_str'] = item.pop('gamer_name')
        item['gamer_id_str'] = item.pop('gamer_id')
       
        if item['score_int']:
            item['score_int'] = int(item['score_int'])
        if item['rank_int']:
            item['rank_int'] = int(item['rank_int'])
        if item.get('special_int') is not None:
            item['special_int'] = int(item['special_int'])

    return_me = {
        "leaderboard_item_arr": data
    }
    return return_me

    
#uncomment the line below to test locally before deployment
#print(lambda_handler({}, None))


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
