import time
import json
import boto3
import os
from game_objects import Player

class GameStateManager:
    def __init__(self, game, dynamodb, table_name):
        self.game = game
        self.game_id = self.game.game_id
        self.dynamodb = dynamodb
        self.table_name = table_name

    def _game_update_expression(self, time_to_live):
        
        return {
            "Update": {
                "TableName": self.table_name,
                "Key": {
                    "PK": {"S": f"GAME#{self.game_id}"},
                    "SK": {"S": f"GAME#{self.game_id}"},
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
                    ":started": { "S": str(self.game.game_started) },
                    ":runes_taken": { "N": str(self.game.runes_taken) },
                    ":game_over": { "BOOL": self.game.game_over },
                    ":turn": { "N": str(self.game.turn) },
                    ":tied": { "BOOL": self.game.tied_game },
                    ":crd_shop": { "S": json.dumps(self.game.card_shop.__dict__()) },
                    ":drg_shop": { "S": json.dumps(self.game.dragon_shop.__dict__()) },
                    ":config": { "S": json.dumps(self.game.config.__dict__()) },
                    ":players": { "N": str(len(self.game.players))},
                    ":ttl": { "N": str(time_to_live) }
                }
            }
        }

    def _player_update_expression(self, player: Player, time_to_live):
        pl_cards = [card['card'].__dict__() for card in player.cards]
        pl_dragons = [dragon.__dict__() for dragon in player.dragons]
        return {
            "Update": {
                "TableName": self.table_name,
                "Key": {
                    "PK": { "S": f"GAME#{self.game_id}" },
                    "SK": { "S": f"USER#{player.sid}" },
                },
                "UpdateExpression": "SET #hp = :hp, #runes = :runes, #affinities = :affinities, \
                                    #cards = :cards, #dragons = :dragons, #vines = :vines, \
                                    #burn = :burn, #display_name = :display_name, #dead = :dead, \
                                    #shield = :shield, #icon = :icon, #xp = :xp, #lvl = :lvl, \
                                    #rewards = :rewards, #time_to_live = :ttl",
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
                    "#xp": "xp",
                    "#lvl": "level",
                    "#rewards": "rewards",
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
                    ":xp": { "N": str(player.xp) },
                    ":lvl": { "N": str(player.lvl) },
                    ":rewards": {"M": {
                                        "common_crates": {"N": str(player.rewards.get('common_crates', 0))},
                                        "keys": {"N": str(player.rewards.get('keys', 0))}
                                    },
                                },
                    ":ttl": { "N": time_to_live }
                }
            }
        }

    def _transact_write(self, transact_items):
        try:
            return self.dynamodb.transact_write_items(TransactItems=transact_items, ReturnConsumedCapacity="INDEXES")
        except Exception as e:
            print(f"Failed to save state: {e}")
            print("FAIL REASON:", e.response.get("CancellationReasons"))
            return None

    def _save_player_state(self, player: Player):
        time_to_live = str(time.time() + 5 * 60 * 60).split(".")[0]
        transact_items = [
            self._game_update_expression(time_to_live),
            self._player_update_expression(player, time_to_live)
        ]
        return self._transact_write(transact_items)

    def _save_state(self):
        time_to_live = str(time.time() + 5 * 60 * 60).split(".")[0]
        transact_items = [self._game_update_expression(time_to_live)]
        for id, player in self.game.players.items():
            transact_items.append(self._player_update_expression(player, time_to_live))
        return self._transact_write(transact_items)

    def _save_user_data(self, players: dict[str, Player]):
        """
        Update all players stats that were in the game
        """
        print("UPDATING USER DATA")
        transact_items = []
        cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        user_pool_id = os.environ['USER_POOL_ID']

        for id, player in players.items():
            username = player.display_name
            sub = player.sid

            # Only persist user data of cognito users
            try:
                response = cognito_client.admin_get_user(
                    UserPoolId=user_pool_id,
                    Username=username
                )
                # Check if the players id matches the sub of the user in Cognito
                if not any(att['Value'] == sub for att in response['UserAttributes']):
                    continue
            except cognito_client.exceptions.UserNotFoundException:
                print(f"No user with Username '{username}' found in the user pool.")
                continue

            wins = 1 if player.won else 0
            dragons_owned = player.dragons_owned
            legendary_cards_bought = player.leg_cards_bought

            xp_req = self.game.xp_system.calc_xp_needed(player)

            # Use ADD expression to increment/add values that don't exist
            transact_items.append(
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": {
                            "PK": { "S": f"USER#{player.sid}" },
                            "SK": { "S": f"USER#{player.sid}" },
                        },
                        "UpdateExpression": "SET #wins = #wins + :wins, \
                                            #dragons = #dragons + :dragons, \
                                            #leg_cards = #leg_cards + :leg_cards, \
                                            #xp = :xp, #lvl = :level, #xp_req = :req_xp, \
                                            #inv.common_crates = #inv.common_crates + :common_crates, \
                                            #inv.#keys = #inv.#keys + :keys",
                        "ExpressionAttributeNames": {
                            "#wins": "total_wins",
                            "#dragons": "dragons_owned",
                            "#leg_cards": "leg_cards_bought",
                            "#xp": "xp",
                            "#lvl": "level",
                            "#xp_req": "required_xp",
                            "#inv": "inventory",
                            "#keys": "keys"
                        },
                        "ExpressionAttributeValues": {
                            ":wins": { "N": str(wins) },
                            ":dragons": { "N": str(dragons_owned)},
                            ":leg_cards": { "N": str(legendary_cards_bought)},
                            ":xp": { "N": str(player.xp)},
                            ":level": { "N": str(player.level)},
                            ":req_xp": { "N": str(xp_req)},
                            ":common_crates": { "N": str(player.rewards.get('common_crates', 0))},
                            ":keys": {"N": str(player.rewards.get('keys', 0))}
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
        return self._transact_write(transact_items)








# class Opulence:
#     def __init__(self):
#         #... other initializations ...
#         self.game_state_manager = GameStateManager(self, self.dynamodb, self.table_name)
