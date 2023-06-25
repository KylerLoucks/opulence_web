from decimal import Decimal
import boto3
from boto3.dynamodb.types import TypeDeserializer
import json
import time
from datetime import datetime
import pprint

# Unique ID with a sortable time prefix
from ulid import ULID

class DynamoDBController:
    def __init__(self):

        self.dynamodb = boto3.client('dynamodb', region_name="us-east-1")

        self.table = "testdatapksk"

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
            TableName='testdatapksk',
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
            TableName='testdatapksk',
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
            TableName='testdatapksk',
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
                'TableName': 'testdatapksk',
                'IndexName': 'OpenGamesIndex',
                'Limit': limit,
                'ReturnConsumedCapacity': 'TOTAL'
            }

            if start_key:
                scan_params['ExclusiveStartKey'] = start_key

            resp = self.dynamodb.scan(**scan_params)
            return resp
        except Exception as e:
            print("failed to scan database: ", e)
            print("REASON: ", e.response.get("CancellationReasons"))
    
    # Deserialize dynamodb data types for more readable dictionaries
    def deserialize(self, data):
        if data is None:
            return

        deserializer = TypeDeserializer()
        deserialized_data = []
        for item in data:
            python_data = {k: deserializer.deserialize(v) for k,v in item.items()}
            deserialized_data.append(python_data)
        return deserialized_data
    
    def convert_decimal_to_int(self, data):
        updated_data = []
        for item in data:
            updated_item = {}
            for key, value in item.items():
                if isinstance(value, Decimal):
                    updated_item[key] = int(value)
                elif isinstance(value, list):
                    updated_item[key] = self.convert_decimal_to_int(value)
                elif isinstance(value, dict):
                    updated_item[key] = self.convert_decimal_to_int(value.values())
                else:
                    updated_item[key] = value
            updated_data.append(updated_item)
        return updated_data



# controller = DynamoDBController()
# data = controller.find_games(3)
# deserialized = controller.deserialize(data.get('Items'))
# pprint.pprint(deserialized)
# pprint.pprint(data)

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