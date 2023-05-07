import json
from Config import Config
from game_objects import *
from shop import *
from game_logs import GameLogs
import datetime
import time
from threading import Timer
import threading


class Opulence:
    def __init__(self, config: Config):
        self.players = dict()
        self.player_sids = []
        self.player_names = []
        self.turn = 0
        self.runes_taken = 0
        self.config = config
        self.card_shop = CardShop(config)
        self.dragon_shop = DragonShop(config)
        self.basic_card_shop = BasicCardShop(config)
        self.game_logs = GameLogs()
        self.game_started = False
        self.game_over = False
        self.turn_timer = None
        self.tied_game = False

    # Update the game state in DynamoDB
    def _save_state(self, players):
        transact_items=[
            {
                "Update": {
                    "TableName": "battle-royale",
                    "Key": {
                        "PK": { f"GAME#{self.game_id}" },
                        "SK": { f"GAME#{self.game_id}" },
                    },
                    "UpdateExpression": "SET #started = :started, #crd_shop = :crd_shop, #drg_shop = :drg_shop",
                    "ExpressionAttributeNames": {
                        "#started": "started",
                        "#crd_shop": "card_shop",
                        "#drg_shop": "dragon_shop",

                    },
                    "ExpressionAttributeValues": {
                        ":started": { "S": self.game_started },
                        ":crd_shop": { "L": self.card_shop.__dict__() },
                        ":drg_shop": { "L": self.dragon_shop.__dict__() }
                    },
                    "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                }
            }
        ]

        for id, player in self.players.items():
            transact_items.append(
                {
                    "Update": {
                        "TableName": "battle-royale",
                        "Key": {
                            "PK": { f"GAME#{self.game_id}" },
                            "SK": { f"USER#{player[id]}" },
                        },
                        "UpdateExpression": "SET #hp = :hp, #runes = :runes, #affinities = :affinities, \
                                            #cards = :cards, #dragons = :dragons, #vines = :vines, \
                                            #burn = :burn, #display_name = :display_name, #dead = :dead, \
                                            #shield = :shield",
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
                            "#shield": "shield"
                        },
                        "ExpressionAttributeValues": {
                            ":hp": { "N": player[id].hp },
                            ":runes": { "M": player[id].runes },
                            ":affinities": { "M": player[id].affinities },
                            ":cards": { "L": player[id].cards },
                            ":dragons": { "L": player[id].dragons },
                            ":vines": { "N": player[id].vines },
                            ":burn": { "N": player[id].burn },
                            ":display_name": { "S": player[id].display_name },
                            ":dead": { "B": player[id].isDead },
                            ":shield": { "M": player[id].shield }, # change this
                        },
                    }
                }
            )

        resp = dynamodb.transact_write_items(TransactItems=transact_items)
        return resp


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
            # self.turn_timer = Timer(self.config.turn_timer, self._next_turn, args=[self.players[self.player_sids[self.turn]], False])
            # Start the timer
            # self.turn_timer.start()
            print(f"Game was started. It's {self.players[sid2].display_name}'s turn")
            return True



    def add_player(self, sid: str, name: str=None):
        num_players = len(self.players)
        if num_players >= self.config.max_players \
                or sid in self.players \
                or self.game_started:
            return False
        sid = num_players if sid==None else sid
        self.players[sid] = Player(sid, name=name, hp=self.config.player_starting_health)
        self.player_sids.append(sid)
        self.player_names.append(name)
        self.game_logs.join_game_log(self.players[sid].display_name)
        return True

    def remove_player(self, sid: str, name: str=None, disconnected=False):
        if sid not in self.players:
            return False

        if self.game_over:
            del self.players[sid]
            self.player_sids.remove(sid)
            if name in self.player_names:
                self.player_names.remove(name)
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

    def _next_turn(self, player: Player=None, player_left_during_turn=False):
        """
        player: The player whose turn it was before _next_turn is called.
        """
        # check if the game should end
        if player_left_during_turn:
            if self._check_winner(): # if the game tied or was won (True)
                self.game_over = True
                # self.turn_timer.cancel()
                return
        
        # apply effects at the end of the turn
        if not player_left_during_turn:
            current_player = player
            if current_player.vines > 0:
                self.game_logs.took_poison_dmg = True
                current_player.take_damage(rune.NATURE, 1, self.game_logs)
            if current_player.burn > 0:
                self.game_logs.took_burn_dmg = True
                current_player.take_damage(rune.FIRE, current_player.burn, self.game_logs)
                current_player.burn = 0

            # check if the game should end
            if self._check_winner(): # if the game tied or was won (True)
                self.game_over = True
                # self.turn_timer.cancel()
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
        # self.turn_timer.cancel()
        # self.turn_timer = Timer(self.config.turn_timer, self._next_turn, args=[self.players[self.player_sids[self.turn]], False])
        # self.turn_timer.start()
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
            return True

        if len(players_alive) == 1:
            winner = list(players_alive.values())[0].display_name
            self.game_logs.winner_log(winner)
            self.game_logs.winner = winner
            return True
        return False


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
    

    
