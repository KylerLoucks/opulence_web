import boto3
import json
import time
from datetime import datetime

# Unique ID with a sortable time prefix
from ulid import ULID

class DynamoDBController:
    def __init__(self):

        self.dynamodb = boto3.resource('dynamodb')

        self.table = self.dynamodb.Table("testdatapksk")

# logs = []

# for i in range(5):
#     logs.append(f"averageplayername took 10x :arcane: damage to their shield and 20x :arcane: damage to their health.{i}")
    def update_logs(self):
        try:
            response = self.table.update_item(
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

    # get a game by ID
    def get_game(self, id: str=None):
        response = self.table.get_item(
            Key={
                'PK': f"GAME#{id}",
                'SK': f"GAME#{id}"
            },
            
            ReturnConsumedCapacity='TOTAL',

        )
        return response

    def create_game(self):
        self.table.put_item(

        )

    # Grab game by GameID and the users in the game
    def fetch_game_and_users(self, game_id):
        resp = self.table.query(
            TableName='testdatapksk',
            KeyConditionExpression="PK = :game",
            ExpressionAttributeValues={
                ":game": "GAME#{}".format(game_id),
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity='TOTAL',
        )

        # games = [Game(item) for item in resp['Items']]

        return resp

    # Grab users in a Game by the GameID
    def fetch_users_in_game(self, game_id):
        resp = self.table.query(
            TableName='testdatapksk',
            KeyConditionExpression="PK = :game and begins_with(SK, :user)",
            ExpressionAttributeValues={
                ":game": "GAME#{}".format(game_id),
                ":user": "USER#"
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity='TOTAL',
        )

        # games = [Game(item) for item in resp['Items']]

        return resp

# games = fetch_users_in_game(game_id="01GPEV315ASJQK3PRMAW94XCQG")
# print(f"Users in GameID '01GPEV315ASJQK3PRMAW94XCQG':\n {games}")

    def find_Joinable_games(self, limit):
        resp = self.table.query(
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

        # games = [Game(item) for item in resp['Items']]

        return resp


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