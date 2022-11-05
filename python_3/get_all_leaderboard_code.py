import boto3, json
from boto3.dynamodb.conditions import Key, Attr, Not

TABLE_NAME_STR = 'LeaderBoard'
INDEX_NAME_STR = 'special_GSI'
DDB = boto3.resource('dynamodb', region_name='us-east-1')
TABLE = DDB.Table(TABLE_NAME_STR)
    
def lambda_handler(event, context):
   # determine which api call was made
    path_str = event.get('path')
    #if '/leaderboard' was called scan entire table:
    if path_str == "/leaderboard":
        return scan_table(event, context)
    else:
        # return top gamers with score greater than 3000
        response = TABLE.query(
            IndexName=INDEX_NAME_STR,
            ScanIndexForward=False,
            KeyConditionExpression=Key('special').eq(1) & Key('score').gt(3000),
            #KeyConditionExpression=Key('score').gt(3000),
            #FilterExpression=Attr("score").gte(3000)
        )
        
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
    
def scan_table(event, context):

    print("Running scan on index...")
    ## event and context not used
    TABLE = DDB.Table(TABLE_NAME_STR)

    
    response = TABLE.scan()

    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = TABLE.scan()
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