import json
from Config import Config
from game_objects import *
from shop import CardShop, DragonShop, BasicCardShop
from game_logs import GameLogs
from datetime import datetime
import time
from threading import Timer
import threading
import boto3
import ulid
from enums import Rune
import pprint
import os
from dotenv import load_dotenv
ENV = os.environ.get("PYTHON_ENV", "dev")
load_dotenv(f'.env.python.{ENV}')

class Opulence:
    def __init__(self, config: Config, game_id: str=None):
        self.game_id = str(ulid.ULID()) if not game_id else game_id
        self.players = dict()
        self.player_sids = []
        self.player_names = []
        self.turn = 0
        self.runes_taken = 0
        self.config = config
        self.card_shop = CardShop(config=config)
        self.dragon_shop = DragonShop(config=config)
        self.basic_card_shop = BasicCardShop(config=config)
        self.game_logs = GameLogs()
        self.game_started = False
        self.game_over = False
        self.turn_timer = None
        self.tied_game = False
        
        # check if only a card or rune was purchased/taken
        self.boring_turn = False

        self.dynamodb = boto3.client('dynamodb', region_name="us-east-1")
        self.table_name = os.environ['DDB_TABLE'] # "testdatapksk"

    def _save_player_state(self, player):
        """
        Save only the game state and a specific players state.
        Useful for when other players had no state changes.
        """
        self.boring_turn = False
        time_to_live = str(time.time() + 5 * 60 * 60).split(".")[0]

        transact_items=[
            {
                # Update Game record
                "Update": {
                    "TableName": self.table_name,
                    "Key": {
                        "PK": { "S": f"GAME#{self.game_id}" },
                        "SK": { "S": f"GAME#{self.game_id}" },
                    },
                    "UpdateExpression": "SET #started = :started, #rt = :runes_taken, #go = :game_over, \
                                        #tied = :tied, #turn = :turn, #crd_shop = :crd_shop, \
                                        #drg_shop = :drg_shop, #time_to_live = :ttl, #game_config = :config, \
                                        #players = :players",
                    "ExpressionAttributeNames": {
                        "#started": "started",
                        "#go": "game_over",
                        "#tied": "tied_game",
                        "#turn": "turn",
                        "#rt": "runes_taken",
                        "#crd_shop": "card_shop",
                        "#drg_shop": "dragon_shop",
                        "#time_to_live": "TTL",
                        "#game_config": "config",
                        "#players": "players"

                    },
                    "ExpressionAttributeValues": {
                        ":started": { "S": str(self.game_started) },
                        ":runes_taken": { "N": str(self.runes_taken) },
                        ":game_over": { "BOOL": self.game_over },
                        ":turn": { "N": str(self.turn) },
                        ":tied": { "BOOL": self.tied_game },
                        ":crd_shop": { "S": json.dumps(self.card_shop.__dict__()) },
                        ":drg_shop": { "S": json.dumps(self.dragon_shop.__dict__()) },
                        ":config": { "S": json.dumps(self.config.__dict__()) },
                        ":players": { "N": str(len(self.players))},
                        ":ttl": { "N": str(time_to_live) }
                    }
                }
            }
        ]

        # JSON serialize the players cards and dragon objects
        pl_cards = [card['card'].__dict__() for card in player.cards]
        pl_dragons = [dragon.__dict__() for dragon in player.dragons]

        transact_items.append(
            {
                "Update": {
                    "TableName": self.table_name,
                    "Key": {
                        "PK": { "S": f"GAME#{self.game_id}" },
                        "SK": { "S": f"USER#{player.sid}" },
                    },
                    "UpdateExpression": "SET #hp = :hp, #runes = :runes, #affinities = :affinities, \
                                        #cards = :cards, #dragons = :dragons, #vines = :vines, \
                                        #burn = :burn, #display_name = :display_name, #dead = :dead, \
                                        #shield = :shield, #icon = :icon \
                                        #time_to_live = :ttl",
                    "ExpressionAttributeNames": {
                        "#hp": "hp",
                        "#runes": "runes",
                        "#affinities": "affinities",
                        "#cards": "cards",
                        "#dragons": "dragons",
                        "#vines": "vines",
                        "#burn": "burn",
                        "#display_name": "display_name",
                        "#dead": "is_dead",
                        "#shield": "shield",
                        "#icon": "icon",
                        "#time_to_live": "TTL"
                    },
                    "ExpressionAttributeValues": {
                        ":hp": { "N": str(player.hp) },
                        ":runes": { "S": json.dumps(player.runes) },
                        ":affinities": { "S": json.dumps(player.affinities) },
                        ":cards": { "S": json.dumps(pl_cards) },
                        ":dragons": { "S": json.dumps(pl_dragons) },
                        ":vines": { "N": str(player.vines) },
                        ":burn": { "N": str(player.burn) },
                        ":display_name": { "S": player.display_name },
                        ":dead": { "BOOL": player.isDead },
                        ":shield": { "S": json.dumps(player.shield.__dict__()) },
                        ":icon": { "S": player.icon },
                        ":ttl": { "N": time_to_live}
                    },
                }
            }
        )
        try:
            resp = self.dynamodb.transact_write_items(TransactItems=transact_items, ReturnConsumedCapacity="INDEXES")
        except Exception as e:
            print("Failed to save individual player game state", e)
            print("FAIL REASON: ", e.response.get("CancellationReasons"))
            return None
        return resp
    

    def _delete_player_state(self, player_sid):
        """
        Delete a players state from the database.
        """
        self.boring_turn = False
        time_to_live = str(time.time() + 5 * 60 * 60).split(".")[0]

        transact_items=[
            {
                # Update Game record
                "Update": {
                    "TableName": self.table_name,
                    "Key": {
                        "PK": { "S": f"GAME#{self.game_id}" },
                        "SK": { "S": f"GAME#{self.game_id}" },
                    },
                    "UpdateExpression": "SET #started = :started, #rt = :runes_taken, #go = :game_over, \
                                        #tied = :tied, #turn = :turn, #crd_shop = :crd_shop, \
                                        #drg_shop = :drg_shop, #time_to_live = :ttl, #game_config = :config, \
                                        #players = :players",
                    "ExpressionAttributeNames": {
                        "#started": "started",
                        "#go": "game_over",
                        "#tied": "tied_game",
                        "#turn": "turn",
                        "#rt": "runes_taken",
                        "#crd_shop": "card_shop",
                        "#drg_shop": "dragon_shop",
                        "#time_to_live": "TTL",
                        "#game_config": "config",
                        "#players": "players"

                    },
                    "ExpressionAttributeValues": {
                        ":started": { "S": str(self.game_started) },
                        ":runes_taken": { "N": str(self.runes_taken) },
                        ":game_over": { "BOOL": self.game_over },
                        ":turn": { "N": str(self.turn) },
                        ":tied": { "BOOL": self.tied_game },
                        ":crd_shop": { "S": json.dumps(self.card_shop.__dict__()) },
                        ":drg_shop": { "S": json.dumps(self.dragon_shop.__dict__()) },
                        ":config": { "S": json.dumps(self.config.__dict__()) },
                        ":players": { "N": str(len(self.players))},
                        ":ttl": { "N": str(time_to_live) }
                    }
                }
            }
        ]

        transact_items.append(
            {
                "Delete": {
                    "TableName": self.table_name,
                    "Key": {
                        "PK": { "S": f"GAME#{self.game_id}" },
                        "SK": { "S": f"USER#{player_sid}" },
                    },
                }
            }
        )
        try:
            resp = self.dynamodb.transact_write_items(TransactItems=transact_items, ReturnConsumedCapacity="INDEXES")
        except Exception as e:
            print("Failed to Delete individual player from the game state", e)
            print("FAIL REASON: ", e.response.get("CancellationReasons"))
            return None
        return resp

    def _save_state(self):
        """
        Save the game state and state of all players in the game.
        """

        # unix epoch time format 5 hours from now without milliseconds
        time_to_live = str(time.time() + 5 * 60 * 60).split(".")[0]
        transact_items=[
            {
                # Update Game record
                "Update": {
                    "TableName": self.table_name,
                    "Key": {
                        "PK": { "S": f"GAME#{self.game_id}" },
                        "SK": { "S": f"GAME#{self.game_id}" },
                    },
                    "UpdateExpression": "SET #started = :started, #rt = :runes_taken, #go = :game_over, \
                                        #tied = :tied, #turn = :turn, #crd_shop = :crd_shop, \
                                        #drg_shop = :drg_shop, #time_to_live = :ttl, #game_config = :config, \
                                        #players = :players",
                    "ExpressionAttributeNames": {
                        "#started": "started",
                        "#go": "game_over",
                        "#tied": "tied_game",
                        "#turn": "turn",
                        "#rt": "runes_taken",
                        "#crd_shop": "card_shop",
                        "#drg_shop": "dragon_shop",
                        "#time_to_live": "TTL",
                        "#game_config": "config",
                        "#players": "players"

                    },
                    "ExpressionAttributeValues": {
                        ":started": { "S": str(self.game_started) },
                        ":runes_taken": { "N": str(self.runes_taken) },
                        ":game_over": { "BOOL": self.game_over },
                        ":turn": { "N": str(self.turn) },
                        ":tied": { "BOOL": self.tied_game },
                        ":crd_shop": { "S": json.dumps(self.card_shop.__dict__()) },
                        ":drg_shop": { "S": json.dumps(self.dragon_shop.__dict__()) },
                        ":config": { "S": json.dumps(self.config.__dict__()) },
                        ":players": { "N": str(len(self.players))},
                        ":ttl": { "N": str(time_to_live) }
                    }
                }
            }
        ]

        # For each player in the game, update their records
        for id, player in self.players.items():

            # JSON serialize the players cards and dragon objects
            pl_cards = [card['card'].__dict__() for card in player.cards]
            pl_dragons = [dragon.__dict__() for dragon in player.dragons]

            transact_items.append(
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": {
                            "PK": { "S": f"GAME#{self.game_id}" },
                            "SK": { "S": f"USER#{player.sid}" },
                        },
                        "UpdateExpression": "SET #hp = :hp, #runes = :runes, #affinities = :affinities, \
                                            #cards = :cards, #dragons = :dragons, #vines = :vines, \
                                            #burn = :burn, #display_name = :display_name, #dead = :dead, \
                                            #shield = :shield, #icon = :icon, \
                                            #time_to_live = :ttl",
                        "ExpressionAttributeNames": {
                            "#hp": "hp",
                            "#runes": "runes",
                            "#affinities": "affinities",
                            "#cards": "cards",
                            "#dragons": "dragons",
                            "#vines": "vines",
                            "#burn": "burn",
                            "#display_name": "display_name",
                            "#dead": "is_dead",
                            "#shield": "shield",
                            "#icon": "icon",
                            "#time_to_live": "TTL"
                        },
                        "ExpressionAttributeValues": {
                            ":hp": { "N": str(player.hp) },
                            ":runes": { "S": json.dumps(player.runes) },
                            ":affinities": { "S": json.dumps(player.affinities) },
                            ":cards": { "S": json.dumps(pl_cards) },
                            ":dragons": { "S": json.dumps(pl_dragons) },
                            ":vines": { "N": str(player.vines) },
                            ":burn": { "N": str(player.burn) },
                            ":display_name": { "S": player.display_name },
                            ":dead": { "BOOL": player.isDead },
                            ":shield": { "S": json.dumps(player.shield.__dict__()) },
                            ":icon": { "S": player.icon },
                            ":ttl": { "N": time_to_live }
                        }
                    }
                }
            )
        try:
            resp = self.dynamodb.transact_write_items(TransactItems=transact_items, ReturnConsumedCapacity="INDEXES")
        except Exception as e:
            print("Failed to save game state", e)
            return None
        return resp
    
    def _load_game_state(self):
        """
        Query DynamoDB for game and user data
        """

        # Grab game data and users
        resp = self.dynamodb.query(
            TableName=self.table_name,
            KeyConditionExpression="PK = :game",
            ExpressionAttributeValues={
                ":game": { "S": "GAME#{}".format(self.game_id) },
            },
            ScanIndexForward=True,
            ReturnConsumedCapacity='TOTAL',
        )
        game_data = resp['Items'][0]
        player_data = resp['Items'][1:]

        # Parse the stringified json that was dumped during '_save_state()'
        card_shop_data      = json.loads(game_data['card_shop']['S'])
        dragon_shop_data    = json.loads(game_data['dragon_shop']['S'])
        config              = json.loads(game_data['config']['S'])
        self.config         = Config(
                                max_players=config['max_players'],
                                cards_in_shop=config['cards_in_shop'],
                                runes_per_turn=config['runes_per_turn'],
                                dragons_in_shop=config['drags_in_shop'],
                                player_starting_health=config['starting_hp'],
                                turn_timer=config['turn_timer'])
        self.card_shop      = CardShop(data=card_shop_data['cards'], config=self.config)
        self.dragon_shop    = DragonShop(data=dragon_shop_data['dragons'], config=self.config)
        self.game_over      = game_data['game_over']['BOOL']
        boolean_value       = game_data['started']['S'].lower() == 'true'
        self.game_started   = boolean_value
        self.turn           = int(game_data['turn']['N'])
        self.tied_game      = game_data['tied_game']['BOOL']
        self.runes_taken    = int(game_data['runes_taken']['N'])

        # Update each players state
        for index, player in enumerate(player_data):
            sid = player['SK']['S'].split('USER#')[1]
            name = player['display_name']['S']
            icon = player['icon']['S']
            self.players[sid] = Player(sid, name=name, icon=icon, data=player_data[index])
            self.player_sids.append(sid)




    def _get_game_data(self):
        users = []
        for player in self.players:
            users.append(self.players[player].__dict__())

        data = {
            "user_data": users,
            "card_shop": self.card_shop.__dict__()
        }

        return data

    def _get_dragon_shop_data(self):
        data = self.dragon_shop.__dict__()
        return data

    def start_game(self, sid):
        """
        - params sid: the sid of the person who started the game
        """
        if self.game_started:
            return False
        else: 
            self.game_started = True
            sid2 = self.player_sids[self.turn] # the sid of the player whose turn it will be when the game starts
            self.game_logs.start_game_log(self.players[sid].display_name, self.players[sid2].display_name)

            # Create a timer thread to run _next_turn() after x seconds
            self.turn_timer = Timer(self.config.turn_timer, self._next_turn, args=[self.players[self.player_sids[self.turn]], False, True])
            # Start the timer
            self.turn_timer.start()
            # self.turn_timer.start()
            print(f"Game was started. It's {self.players[sid2].display_name}'s turn")
            return True


    # TODO: Remove player_names field
    def add_player(self, sid: str, name: str=None, icon: str=None):
        num_players = len(self.players)
        if num_players >= self.config.max_players \
                or sid in self.players \
                or self.game_started:
            return False
        sid = num_players if sid==None else sid
        self.players[sid] = Player(sid, name=name, icon=icon, hp=self.config.player_starting_health)
        self.player_sids.append(sid)
        self.player_names.append(name)
        self.game_logs.join_game_log(self.players[sid].display_name)
        self._save_player_state(player=self.players[sid])
        return True

    def remove_player(self, sid: str, name: str=None, disconnected=False):
        if sid not in self.players:
            return False

        if self.game_over:
            del self.players[sid]
            self.player_sids.remove(sid)
            if name in self.player_names:
                self.player_names.remove(name)

            self._delete_player_state(player_sid=sid)
            return True
        
        
        
        if self.game_started:
            current_player = self.player_sids[self.turn] if len(self.player_sids) > 1 else self.player_sids[0]
            # /// handle if the game is in progress and it's the players turn \\\
            if sid == current_player: 
                self.game_logs.leave_game_log(self.players[sid].display_name, while_started=True, disconnected=disconnected)
                print(f"player left the game while it was their turn: {name}")
                del self.players[sid]
                if name in self.player_names:
                    self.player_names.remove(name)

                self._delete_player_state(player_sid=sid)
                self._next_turn(player_left_during_turn=True)
                return True
            else:
                print(f"player left the game: {name}")
                self.game_logs.leave_game_log(self.players[sid].display_name, disconnected=disconnected)
                del self.players[sid]
                if name in self.player_names:
                    self.player_names.remove(name)
                return True
        else: 
            print(f"player left the game before the game started: {name}")
            self.game_logs.leave_game_log(self.players[sid].display_name, disconnected=disconnected)
            del self.players[sid]
            self.player_sids.remove(sid)
            if name in self.player_names:
                self.player_names.remove(name)
            self._delete_player_state(player_sid=sid)
            return True

    def take_rune(self, sid: str, rune: str):
        """
        sid: the player sid taking the rune
        rune: name of the rune (string)
        """
        # if the game ended
        if self.game_over:
            return False

        if not self.game_started:
            return False

        # if it isn't the players turn
        if sid not in self.players or sid != self.player_sids[self.turn]:
            return False
        self.players[sid].runes[rune] += 1
        self.runes_taken += 1
        if self.runes_taken >= self.config.runes_per_turn:
            self.game_logs.take_rune_log(self.players[sid].display_name, rune) # maybe ? add a boolean to say something different when the turn ends on this action
            self.boring_turn = True
            self._next_turn(self.players[sid])
            return True
        else:
            self.game_logs.take_rune_log(self.players[sid].display_name, rune)
            return True

    def buy_card(self, sid, card_idx):
        """
        card_idx: the position of the card in the shop
        sid : player sid of the person buying the card
        """
        # if the game ended
        if self.game_over:
            return False

        # if it isn't the players turn
        if sid not in self.players or sid != self.player_sids[self.turn]: 
            return False
        # if the player has already started taking runes
        if self.runes_taken > 0:
            # Maybe return the log to tell the player they can't do this
            return False
        if self.card_shop.buy(self.players[sid], card_idx, self.game_logs):
            # buy() adds the card to the players hand
            self.players[sid].update_affinities()
            self.boring_turn = True
            self._next_turn(self.players[sid])
            return True
        
    def buy_basic_card(self, sid, element1, element2):
        """
        elements 1&2 : the elements to spend crafting the card
        sid : player sid of the person crafting the card
        """
        # if the game ended
        if self.game_over:
            return False

        # if it isn't the players turn
        if sid not in self.players or sid != self.player_sids[self.turn]: 
            return False
        # if the player has already started taking runes
        if self.runes_taken > 0:
            # Maybe return the log to tell the player they can't do this
            return False
        # if the player tried to take the same 2 elements (packet hacking)
        if element1 == element2:
            return False
        if element1 == 'none' or element2 == 'none':
            return False
        if self.basic_card_shop.buy(self.players[sid], element1, element2, self.game_logs):
            # buy() adds the card to the players hand
            self.players[sid].update_affinities()
            self.boring_turn = True
            self._next_turn(self.players[sid])
            return True
    
    def buy_dragon(self, sid, card_idx):
        """
        dragon_idx: the position of the dragon in the shop
        sid : player sid of the person buying the dragon
        """
        # if the game ended
        if self.game_over:
            return False

        # if it isn't the players turn
        if sid not in self.players or sid != self.player_sids[self.turn]: 
            return False
        # if the player has already started taking runes
        if self.runes_taken > 0:
            return False
        
        # add the dragon to the player
        if self.dragon_shop.buy(self.players[sid], card_idx):
            self.boring_turn = True
            self._next_turn(self.players[sid])
            return True

    def play_card(self, card_idx, sid1, sid2=None):
        """
        card_idx: the position of the card in sid1's hand
        sid1, sid2: player ids
        """
        # if the game ended
        if self.game_over:
            return False

        if self.runes_taken > 0:
            # Maybe return the log to tell the player they can't do this
            return False

        if sid1 not in self.players or sid1 != self.player_sids[self.turn]:
            return False

        player1 = self.players[sid1]
        player2 = self.players.get(sid2, None)

        # if another player was selected and they turned out to be dead, return false
        if player2 and self.players[sid2].isDead:
            return False
        
        if card_idx > len(player1.cards):
            return False


        card = player1.cards.pop(card_idx)
        self.game_logs.play_card_log(card['card'], player1, player2)
        card_activated = card['card'].activate(player1, player2, self._get_living_players(), self.game_logs)
        if card_activated:
            player1.update_affinities()
            self._next_turn(self.players[sid1])
            return True
        else:
            print("card didn't activate")
            return False

    def get_player_stats(self):
        """
        return the player id, hp, and shield of each player
        """
        return {
            id:{"hp": p.hp, "shield": p.shield.__dict__()} \
            for id, p in self.players.items()
        }

    def _next_turn(self, player: Player=None, player_left_during_turn=False, timer_expired=False):
        """
        player: The player whose turn it was before _next_turn is called.
        """
        # check if the game should end
        if player_left_during_turn:
            if self._check_winner(): # if the game tied or was won (True)
                self.game_over = True
                self.turn_timer.cancel()
                return
        
        # apply effects at the end of the turn
        if not player_left_during_turn:
            current_player = player
            if current_player.vines > 0:
                self.game_logs.took_poison_dmg = True
                current_player.take_damage(Rune.NATURE, 1, self.game_logs)
            if current_player.burn > 0:
                self.game_logs.took_burn_dmg = True
                current_player.take_damage(Rune.FIRE, current_player.burn, self.game_logs)
                current_player.burn = 0

            # check if the game should end
            if self._check_winner(): # if the game tied or was won (True)
                self.game_over = True
                self.turn_timer.cancel()
                return

        # cycle cards in the shop
        self.card_shop.cycle()
        self.runes_taken = 0

        print(f"_next_turn() called. Turn index was: {self.turn}")
        # iterate the turn      
        # loop through all the players that were in the game when it started and iterate the turn until the turn index lands on a player who isn't dead.
        for i in range(0, len(self.player_sids)):
            self.turn = (self.turn+1) % len(self.player_sids) # Iterate the turn index or make it 0 if greater than len of players who were in-game
            if not self.player_sids[self.turn] in self.players: # if the player is not still in game, iterate the turn again
                continue
            elif self.players[self.player_sids[self.turn]].isDead: # if the new player is dead, iterate the turn again
                continue
            else: # if the new player isn't dead, break out of the loop
                break

        print(f"Turn index is now: {self.turn}")
        next_player= self.players[self.player_sids[self.turn]].display_name
        print(f"It's {next_player}'s turn")
        self.game_logs.next_turn_log(str(next_player))

        # Save game state:
        self._save_player_state(player=player) if self.boring_turn else print(self._save_state())
        
        if timer_expired:
            from main import emit_game_turn
            emit_game_turn(self, self.game_id)
        # Restart the turn timer
        self.turn_timer.cancel()
        self.turn_timer = Timer(self.config.turn_timer, self._next_turn, args=[self.players[self.player_sids[self.turn]], False, True])
        self.turn_timer.start()
        print(f"Active threads: {len(threading.enumerate())} ")
    

    def _get_living_players(self):
        """
        return the players that are of the living
        """
        players_with_hp = {}

        for sid, playerstats in self.players.items():
            if self.players[sid].hp > 0:
                players_with_hp[sid] = playerstats

        # return dict of players with hp
        return players_with_hp

    def _get_current_turn_sid(self) -> str:
        """
        Return the sid of the player whose turn it is
        """
        # return self.player_sids[self.turn]

        # return list(self._get_living_players().keys())[self.turn]
        return self.players[self.player_sids[self.turn]].sid
    

    def _check_winner(self):
        """
        return the player id of the player who won
        """
        if not self.game_started:
            return False

        players_alive = self._get_living_players()

        # everyone has 0 hp
        if not players_alive:
            self.game_logs.winner_log(sid=None)
            self.tied_game = True
            self._update_user_data()
            return True

        if len(players_alive) == 1:
            winner = list(players_alive.values())[0].display_name
            list(players_alive.values())[0].won = True
            self.game_logs.winner_log(winner)
            self.game_logs.winner = winner
            self._update_user_data()
            return True
        return False
    
    def _update_user_data(self):
        """
        Update all players stats that were in the game
        """
        print("UPDATING USER DATA")
        transact_items = []
        cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        user_pool_id = os.environ['USER_POOL_ID']

        for id, player in self.players.items():
            username = player.display_name
            sub = player.sid

            # Only persist user data of cognito users
            try:
                response = cognito_client.admin_get_user(
                    UserPoolId=user_pool_id,
                    Username=username
                )
                # Check if the players id matches the sub of the user in Cognito
                if any(att['Value'] == sub for att in response['UserAttributes']):
                    print(f"User with ID '{sub}' matches the 'sub' attribute.")
                else:
                    continue
            except cognito_client.exceptions.UserNotFoundException:
                print(f"No user with Username '{username}' found in the user pool.")
                continue

            wins = 1 if player.won else 0
            dragons_owned = player.dragons_owned
            legendary_cards_bought = player.leg_cards_bought

            # Use ADD expression to increment/add values that don't exist
            transact_items.append(
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": {
                            "PK": { "S": f"USER#{player.sid}" },
                            "SK": { "S": f"USER#{player.sid}" },
                        },
                        "UpdateExpression": "ADD #wins :wins, \
                                            #dragons :dragons, \
                                            #leg_cards :leg_cards",
                        "ExpressionAttributeNames": {
                            "#wins": "total_wins",
                            "#dragons": "dragons_owned",
                            "#leg_cards": "leg_cards_bought",
                        },
                        "ExpressionAttributeValues": {
                            ":wins": { "N": str(wins) },
                            ":dragons": { "N": str(dragons_owned)},
                            ":leg_cards": { "N": str(legendary_cards_bought)}
                        },
                    }
                },
            )

            # Update the users game history with details on the game
            transact_items.append(
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": {
                            "PK": { "S": f"USER#{player.sid}" },
                            "SK": { "S": f"GAME#{player.sid}" },
                        },
                        "UpdateExpression": "SET #won = :won, \
                                            #dragons = :dragons, \
                                            #leg_cards = :leg_cards \
                                            ",
                        "ExpressionAttributeNames": {
                            "#won": "won",
                            "#dragons": "dragons_owned",
                            "#leg_cards": "leg_cards_bought",
                        },
                        "ExpressionAttributeValues": {
                            ":won": { "BOOL": player.won },
                            ":dragons": { "N": str(dragons_owned)},
                            ":leg_cards": { "N": str(legendary_cards_bought)}
                        },
                    }
                }
            )
        try:
            resp = self.dynamodb.transact_write_items(TransactItems=transact_items, ReturnConsumedCapacity="INDEXES")
        except Exception as e:
            print("Failed to save game state", e)
            # print("REASON: ", e.response.get("CancellationReasons"))
            return None
        return resp

if __name__ == "__main__":
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
    # o.players["player1"].set_runes()
    # o._get_game_data()
    # o.players["player1"].add_dragon()
    # o._get_game_data()
    # o.game_logs.take_rune_log("1", rune.FIRE)

    # o.players["player1"].isDead = True
    # o._next_turn(o.players["player4"])
    # o._get_game_data()
    

    