import json
from Config import Config
from game_objects import *
from opulence import Opulence
from dynamodb_controller import DynamoDBController
# from shop import *
# from game_logs import GameLogs
import datetime
import time
from threading import Timer
import threading
import boto3


def test_threading_turn_timer():
    games = {}
    for i in range(0, 50):
        o = Opulence(Config())
        o.add_player("player1")
        o.add_player("player2")
        o.add_player("player3")
        o.add_player("player4")
        
        o.start_game("player1")
        print("player took a rune")
        o.take_rune("player1", rune="FIRE")
        print("Waiting.....")
        # games[i] = o
    print(games)

def test_basic_game():
    o = Opulence(Config())
    o.add_player("player1")
    o.add_player("player2")
    o.start_game("player1")
    print(o.player_sids)

# Saving and loading state to dynamodb
def test_dynamodb_save_state():
    o = Opulence(config=Config())
    o.add_player("player2")      
    o.add_player("player1")
    o.players['player1'].add_card()
    o.players['player1'].add_dragon()
    o.start_game('player1')
    o._next_turn(o.players["player2"])

def test_dynamodb_load_state():
    o = Opulence(Config(), "01H2PPY91DSBKDW6WBY5E85TKM") # Copy the ID from dynamo after running test_save_state()
    o._load_game_state()
    print(o.player_sids)

def test_dynamodb_controller():
    ddb = DynamoDBController()
    response = ddb.find_games(limit=1)
    last_key = response.get('LastEvaluatedKey')
    deserialized = ddb.deserialize(data=response['Items'])
    data = ddb.convert_decimal_to_int(deserialized)
    return data


if __name__ == "__main__":
    test_dynamodb_save_state()

    # test_dynamodb_load_state()
    # test_basic_game()
    # games = test_dynamodb_controller()
    # print("GAMES", games['Items'])
    print("working!")
    
    # games[i] = o
    
    # o.players["player1"].set_runes()
    # o._get_game_data()
    # o.players["player1"].add_dragon()
    # o._get_game_data()
    # o.game_logs.take_rune_log("1", Rune.FIRE)

    # o.players["player1"].isDead = True
    # o._next_turn(o.players["player4"])
    # o._get_game_data()