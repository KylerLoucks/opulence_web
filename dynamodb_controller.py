from decimal import Decimal
import boto3
from boto3.dynamodb.types import TypeDeserializer
import json
import time
from datetime import datetime
import pprint
import os
from dotenv import load_dotenv
# Unique ID with a sortable time prefix
from ulid import ULID

ENV = os.environ.get("PYTHON_ENV", "dev")
load_dotenv(f'.env.python.{ENV}')

class DynamoDBController:
    def __init__(self):

        self.dynamodb = boto3.client('dynamodb', region_name="us-east-1")

        self.table = os.environ['DDB_TABLE'] # "testdatapksk"

# logs = []

# for i in range(5):
#     logs.append(f"averageplayername took 10x :arcane: damage to their shield and 20x :arcane: damage to their health.{i}")
    def update_logs(self):
        try:
            response = self.dynamodb.update_item(
                    Key={
                        'PK': 'GAME#12345'
                    },
                    # Append :logValue list to 'game_logs' attribute list
                    UpdateExpression="SET gameLogs = list_append(if_not_exists(gameLogs, :emptyVal), :logVal)", 
                    ExpressionAttributeValues={
                        ':logVal': ['log1'],
                        ':emptyVal': []
                    },
                    ReturnConsumedCapacity='TOTAL',
                    ConditionExpression='attribute_exists(logs)'
                )
        except Exception as e:
            return "Couldn't update item"
        return response

    # get a game by ID (useful for searching for a single game to join)
    def get_game(self, id: str=None):
        response = self.dynamodb.get_item(
            Key={
                'PK': f"GAME#{id}",
                'SK': f"GAME#{id}"
            },
            
            ReturnConsumedCapacity='TOTAL',

        )
        return response

    # Grab game by GameID and the users in the game
    def fetch_game_and_users(self, game_id):
        resp = self.dynamodb.query(
            TableName=self.table,
            KeyConditionExpression="PK = :game",
            ExpressionAttributeValues={
                ":game": "GAME#{}".format(game_id),
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity='TOTAL',
        )

        return resp

    # Grab users in a Game by the GameID
    def fetch_users_in_game(self, game_id):
        resp = self.dynamodb.query(
            TableName=self.table,
            KeyConditionExpression="PK = :game and begins_with(SK, :user)",
            ExpressionAttributeValues={
                ":game": "GAME#{}".format(game_id),
                ":user": "USER#"
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity='TOTAL',
        )

        return resp

    def find_Joinable_games(self, limit):
        resp = self.dynamodb.query(
            TableName=self.table,
            IndexName='OpenGamesIndex',
            KeyConditionExpression="#started = :startedVal",
            ExpressionAttributeNames={
                "#started": "started",
                # "#players": "players"
            },
            ExpressionAttributeValues={
                ":startedVal": "true"
                # ":playersVal": 1
            },
            ScanIndexForward=True,
            Limit=limit,
            ReturnConsumedCapacity='TOTAL',
        )
        return resp
    
    # Find all games that are currently active
    def find_games(self, limit, start_key=None):
        try:
            scan_params = {
                'TableName': self.table,
                'IndexName': 'OpenGamesIndex',
                'Limit': limit,
                'ReturnConsumedCapacity': 'TOTAL',
            }

            if start_key:
                scan_params['ExclusiveStartKey'] = start_key

            resp = self.dynamodb.scan(**scan_params)
            return resp
        except Exception as e:
            print("failed to scan database: ", e)
            # print("FAIL REASON: ", e.response.get("CancellationReasons"))
    
    def delete_game(self, game_id, users):
        '''
        Delete all game and user records tied to a game.
        '''
        try:
            delete_items = [
                {
                    'PK': { "S": f'GAME#{game_id}' },
                    'SK': { "S": f'GAME#{game_id}' },
                }
            ]

            # for user in users:
            #     delete_items.append(
            #         {
            #             'PK': { "S": f'GAME#{game_id}' },
            #             'SK': { "S": f'USER#{user} }'
            #         }
            #     )
            self.dynamodb.batch_write_item(
                RequestItems={
                    self.table: delete_items
                }
            )

        except Exception as e:
            print("failed to delete game: ", e)

    def get_user_stats(self, userid):
        try:
            response = self.dynamodb.get_item(
                TableName=self.table,
                Key={
                    'PK': {"S": f"USER#{userid}"},
                    'SK': {"S": f"USER#{userid}"}
                },
                
                ReturnConsumedCapacity='TOTAL',

            )
            return response
        except Exception as e:
            print("failed to grab user stats: ", e)

    def change_user_icon(self, userid, icon_name):
        '''
        Updates the users icon with the specified name if they own it.
        '''
        try:
            response = self.dynamodb.update_item(
                TableName=self.table,
                Key={
                    'PK': {"S": f"USER#{userid}"},
                    'SK': {"S": f"USER#{userid}"}
                },
                UpdateExpression="SET icon = :icon_name",
                ConditionExpression="contains(owned_icons, :icon_name)",
                ExpressionAttributeValues={
                    ":icon_name": {"S": icon_name }
                }
            )
            return response
        except Exception as e:
            print("failed to change user icon: ", e)

    def add_new_icon(self, userid, icon_name):
        '''
        Adds a new icon to the list of icons the user owns.
        '''
        try:
            response = self.dynamodb.update_item(
                TableName=self.table,
                Key={
                    'PK': {"S": f"USER#{userid}"},
                    'SK': {"S": f"USER#{userid}"}
                },
                UpdateExpression="SET owned_icons = list_append(owned_icons, :icon_name)",
                ConditionExpression="NOT contains(owned_icons, :icon_name)",
                ExpressionAttributeValues={
                    ":icon_name": {"S": icon_name}
                }
            )
            return response
        except Exception as e:
            print("failed to add a newly owned icon: ", e)

    def open_common_crate(self, userid):
        '''
        Opens a common crate (removes a key and crate from the players inventory).
        Fails if the user doesn't have more than zero keys and crates.
        '''
        try:
            response = self.dynamodb.update_item(
                TableName=self.table,
                Key={
                    'PK': {"S": f"USER#{userid}"},
                    'SK': {"S": f"USER#{userid}"}
                },
                UpdateExpression="SET #inv.common_crates = #inv.common_crates - :one, \
                                    #inv.#keys = #inv.#keys - :one",
                ConditionExpression="#inv.common_crates > :zero and #inv.#keys > :zero",
                ExpressionAttributeNames={
                    "#inv": "inventory",
                    "#keys": "keys"
                },
                ExpressionAttributeValues={
                    ":one": {"N": "-1"},
                    ":zero": {"N": "0"}
                }
            )
            return response
        except Exception as e:
            print("failed to open a crate: ", e)
    
    # Deserialize dynamodb data types for more readable dictionaries
    def deserialize(self, data):
        '''
        Useful for deserializing when making calls with boto3.client. 
        boto3.resource has built-in deserialization.
        '''
        if data is None:
            return

        deserializer = TypeDeserializer()

        # If the data isn't a list:
        if isinstance(data, dict):
            python_data = {k: deserializer.deserialize(v) for k,v in data.items()}
            return python_data
        elif isinstance(data, list):
            deserialized_data = []
            for item in data:
                python_data = {k: deserializer.deserialize(v) for k,v in item.items()}
                deserialized_data.append(python_data)
            return deserialized_data
    
    def convert_decimal_to_int(self, data):
        if isinstance(data, list):
            return [self.convert_decimal_to_int(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.convert_decimal_to_int(value) for key, value in data.items()}
        elif isinstance(data, Decimal):
            return int(data)
        else:
            return data



# ddb = DynamoDBController()
# user = "b8648ae0-0568-4424-b452-c67a51eb8f6"




# item = data['Item']
# deserialize = controller.deserialize(data=item)
# type_convert = controller.convert_decimal_to_int(deserialize)
# pprint.pprint(type_convert)




# last_key = data.get('LastEvaluatedKey')
# data = controller.find_gaames(3, last_key)
# pprint.pprint(data.get('LastEvaluatedKey'))

# data = controller.fetch_game_and_users(game_id="01GPEV315ASJQK3PRMAW94XCQG")
# pprint.pprint(data)


# games = find_Joinable_games(limit=10)
# print(games)

# print("Test")






# def test_datetime():

#     # Current time, splitting and removing the miliseconds
#     start_time = str(datetime.now()).split(".")[0]

#     # unix epoch time format 5 hours from now
#     time_to_live = int(time.time() + 5 * 60 * 60)
    


# def test_ulid():
#     ulid = ULID()

#     return str(ulid)










# doing any action in-game:
    # read game from db

    # create Opulence object with config and and pass config dict from db read
    # opulence.players = db.players
    # opulence.turn = db.turn_index
    # opulence.card_shop.items = db.card_shop_items
    # opulence.dragon_shop.items = db.card_shop_items