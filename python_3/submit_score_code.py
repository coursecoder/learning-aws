import boto3
import uuid

def lambda_handler(event, context):
    # this will create dynamodb resource object and
    # here dynamodb is resource name
    client = boto3.resource('dynamodb')

    # extract the name and score intro local variables
    gamer_name_str = event['gamer_name']
    score_int = event['gamer_score']

    #generte UUID 
    gamer_id_str = str(uuid.uuid4())

    # pass in pre-generated variables
    tags = ['not registered', 'top gamer']
    rank = 1

    # this will search for dynamoDB table 
    table = client.Table("LeaderBoard")
    print(table.table_status)

    #Creating an Item with a unique id and with the passed variables
    table.put_item(
        Item={
            'gamer_name' : gamer_name_str,
            'gamer_id': gamer_id_str,
            'tags' : tags,
            'rank' : rank,
            'score' : int(score_int)
        }
    )

    #return variables
    data = {
        'response_code' : 200,
        'message' : '{}, your score of {} was added!'.format(event['gamer_name'],event['gamer_score']),
        'gamer_id' : gamer_id_str
    }
    return data