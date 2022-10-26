import boto3, json


def batch_put(leaderboard_list):
    DDB = boto3.resource('dynamodb', region_name='us-east-1')
    table = DDB.Table('LeaderBoard')
    with table.batch_writer() as batch:
        for gamer in leaderboard_list:
            gamer_name = gamer['gamer_name_str']
            gamer_id = gamer['gamer_id_str']
            score = gamer['score_int']
            rank = gamer['rank_int']
            tags = gamer['tag_str_arr']
            formatted_data  = {
                'gamer_name': gamer_name,
                'gamer_id': gamer_id,
                'score': score,
                'rank': rank,
                'tags': tags
            }
            # add gamer data and top gamer data
            if 'special_int' in gamer:
                formatted_data['special'] = gamer['special_int']
                print("Adding top gamers:", gamer_name, score)
            else:
                print("Adding gamer:", gamer_name, score)
                pass
           
            batch.put_item(Item=formatted_data)

# Batch upload all leaderboard data to DynamoDB table
if __name__ == '__main__':
    print("Uploading gamer data to DynamoDB table...")
    with open("./resources/website/all_gamers.json") as json_file:
        leaderboard_list = json.load(json_file)['leaderboard_item_arr']
    batch_put(leaderboard_list)

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
