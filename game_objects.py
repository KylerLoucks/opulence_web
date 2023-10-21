import random
import json
from enums import Rune, RUNES, CardType, DragonType
class Shield:
    def __init__(self, rune: Rune=None, power=0):
        self.rune = rune
        self.power = power

    def block(self, element: Rune, power, log, super_effective_multiplier=2.0):
        """
        - param element: the damage type the shield is blocking incoming damage from
        TODO: super_effective_multiplier should come from config?
        """
        multiplier = 1.0
        pairs = {
            (Rune.FIRE, Rune.NATURE),
            (Rune.WATER, Rune.FIRE),
            (Rune.EARTH, Rune.WIND),
            (Rune.NATURE, Rune.EARTH),
            (Rune.SOLAR, Rune.SOLAR),
            (Rune.DARK, Rune.DARK),
            (Rune.WIND, Rune.WATER)
        }

        # arcane goes through shields
        if element == Rune.ARCANE:
            return power

        if element == Rune.WIND:
            # TODO: hard-coded wind damage should come from config?
            multiplier *= 2.0
            log.super_effective = True

        # e.g if the element type is fire and the shield type is nature, apply super effective
        if (element, self.rune) in pairs:
            multiplier *= super_effective_multiplier
            log.super_effective = True
        
        shield_damage = multiplier*power
        damage_left_over = -min(0, (self.power - shield_damage))//multiplier

        # Let the GameLogs Object know how much damage was done to the shield 
        log.damage_to_shield = min(self.power, shield_damage)

        # destroy shield in Player
        self.power -= shield_damage

        return damage_left_over

    def _destroy_shield(self):
        self.rune = None
        self.power = 0

    def __dict__(self):
        return {
            "rune": self.rune.value if self.rune is not None else None,
            "power": self.power
        }

class Player:
    def __init__(self, sid: str, icon: str=None, hp=10, shield: Shield=None, name: str=None, data=None):
        self.sid = sid
        self.icon = "default" if icon == None else icon
        self.hp = hp
        self.shield = Shield() if shield == None else shield
        self.runes = {rune:0 for rune in RUNES}
        self.affinities = {rune:0 for rune in RUNES}
        self.cards = []
        self.dragons = []
        self.isDead = False
        self.display_name = sid if name == None else name
        # status effects, handled elsewhere
        self.vines = 0
        self.burn = 0

        # state to store after the game ends
        self.won = False
        self.leg_cards_bought = 0
        self.dragons_owned = 0

        if data is not None:
            self._populate_from_dynamodb(data)
    
    def _populate_from_dynamodb(self, data):
        """
        Updates the players state to match the state in dynamodb
        data: The payload from dynamodb
        """
        self.hp = int(data['hp']['N'])
        self.isDead = data['is_dead']['BOOL']
        self.display_name = data['display_name']['S']
        self.vines = int(data['vines']['N'])
        self.burn = int(data['burn']['N'])
        self.runes = json.loads(data['runes']['S'])
        self.affinities = json.loads(data['affinities']['S'])
        
        shield_data = json.loads(data['shield']['S'])
        if shield_data['rune'] == None:
            self.shield = Shield()
        else:
            self.shield = Shield(
                rune=Rune[shield_data['rune']],
                power=shield_data['power']
            )

        card_data = json.loads(data['cards']['S'])
        self.cards = [
            {'card': Card(
                    rune=Rune[card['rune']],
                    type=CardType[card['type']],
                    affinity=card['affinity'],
                    power=card['power'])}
            for card in card_data
        ]

        dragon_data = json.loads(data['dragons']['S'])
        self.dragons = [
            Dragon(
                type=DragonType[dragon['type']],
                runes=[Rune[rune] for rune in dragon['runes']])
            for dragon in dragon_data 
        ]

    def update_affinities(self):
        # updated every time a card is bought/played
        self.affinities = {rune:0 for rune in RUNES}
        for card in self.cards:
            self.affinities[card['card'].rune.value] += card['card'].affinity

    def take_damage(self, rune: Rune, power, log):
        """
        rune: str The element type e.g. (Rune.FIRE)
        power: How much base damage to take
        log: GameLogs Object

        returns the amount of damage going to the hp, after blocking with shield
        """
        damage = self.shield.block(rune, power, log)
        log.damage_to_health = min(self.hp, damage)
        self.hp = max(0, self.hp - damage) # hp can't drop below 0
        

        if self.hp <= 0:
            self.isDead = True
            log.player_died=True

        # destroy shield
        if self.shield.power <= 0:
            self.shield = Shield()
            log.shield_destroyed=True
        log.player_took_damage_log(self.display_name, rune)
        return damage

    def get_dragon_multiplier(self, rune_type: Rune=None):
        """
        returns the multiplier a player's dragons give him for a specified rune type
        returns 1.0 if he has no relevant dragons for that element
        """
        mult = 1
        for dragon in self.dragons:
            if rune_type in dragon.runes:
                mult *= 2
        return mult

    def __dict__(self):
        player_cards = []
        if len(self.cards) > 0:
            for card in self.cards:
                dicify_card_obj = card['card'].__dict__()
                player_cards.append({'card': dicify_card_obj})
            
        dragons = []
        if len(self.dragons) > 0:
            for dragon in self.dragons:
                dicify_dragon = dragon.__dict__()
                dragons.append({'dragon': dicify_dragon})
            

        return {
            "sid": self.sid,
            "hp": self.hp,
            "shield": self.shield.__dict__(),
            "runes": self.runes,
            "cards": player_cards,
            "affinities": self.affinities,
            "dragons": dragons,
            "isDead": self.isDead,
            "vines": self.vines,
            "burn": self.burn,
            "display_name": self.display_name,
            "icon": self.icon
        }

    # used for testing
    def add_card(self):
        """
        Add a new Card object to the players cards (list)
        """
        self.cards.append({'card': Card(Rune.EARTH, CardType.SHIELD, 5, 15)})
        self.update_affinities()
   
    # used for testing
    def add_dragon(self):
        """
        Add a new Dragon object to the players dragons (list)
        """
        self.dragons.append(Dragon(type=DragonType.VOID, runes=[Rune.ARCANE, Rune.DARK]))
        self.dragons.append(Dragon(type=DragonType.STEAM, runes=[Rune.ARCANE, Rune.DARK]))

    # for testing
    def set_runes(self):
        self.runes = {rune:20 for rune in RUNES}

    def __str__(self):
        return json.dumps(self.__dict__())



class Dragon:
    """
    Dragon objects that can be held by a player
    - param type: The card type e.g. (DragonType.SOLAR)
    - param runes: The two runes associated with the dragon
    """
    def __init__(self, type: DragonType, runes: list[Rune]):
        self.type = type
        self.runes = runes
    
    def __dict__(self):
        return {
            "type": self.type.value,
            "runes": [rune.value for rune in self.runes],
        }


class Card:
    """
    Card objects that can be held by a player
    - param rune: The element the card is e.g. (rune.FIRE) 
    - param type: The card enum type e.g. (CardType.ATTACK)
    - param affinity: The amount the card is worth in affinity
    - param power: the base amount the card does in damage/shield before modifiers
    """
    def __init__(self, rune: Rune, type: CardType, affinity, power):
        self.rune = rune
        self.type = type
        self.affinity = affinity
        self.power = power

    def __dict__(self):
        return {
            "rune": self.rune.value,
            "type": self.type.value,
            "affinity": self.affinity,
            "power": self.power
        }

    def activate(self, player1: Player, player2, players: dict, log):
        """
        player: instance of Player object for the player of the card
        players: dict of the Player objects
        """
        if self.type == CardType.MUNDANE:
            return False
        elif self.type == CardType.ATTACK:
            return self._activate_attack(player1, player2, players, log)
        elif self.type == CardType.SHIELD:
            return self._activate_shield(player1, log)

    def _activate_shield(self, player, log):
        multiplier = 1.0

        multiplier *= player.get_dragon_multiplier(self.rune)

        power = self.power * multiplier
        shield = Shield(self.rune, power)
        player.shield = shield
        return True




    def _activate_attack(self, player1: Player, player2, players: dict, log):
        multiplier = 1.0
        multiplier *= player1.get_dragon_multiplier(self.rune)

        # if the player playing the card has vines, do the following: 
        # (reduce amount of vines based on the power of the card being played)
        # (reduce the amount of damage the card will do based on how many vines you had)
        if player1.vines > 0:
            fire_bonus = 4.0 if self.rune == Rune.FIRE else 1.0         # fire does 4x damage to vines
            vines_left_over = player1.vines - self.power * multiplier * fire_bonus
            player1.vines = max(0, vines_left_over)
            self.power = -min(0, vines_left_over)//fire_bonus

        # if the card is earth, roll for crit chance
        if self.rune == Rune.EARTH:
            # TODO: hard-coded earth crit chance should come from config?
            crit = random.random() < 0.25
            self.power = self.power*3 if crit else self.power
            if crit:
                print(f"Earth card that was played * CRIT * causing the power to be: {self.power}")

            player2.take_damage(self.rune, self.power * multiplier, log)
            return True

        # if the card is solar, do damage to everyone
        elif self.rune == Rune.SOLAR:
            for player_ in players.values():
                player_.take_damage(self.rune, self.power * multiplier, log)
            return True
        # if the card is dark, heal the player
        elif self.rune == Rune.DARK:
            damage = player2.take_damage(self.rune, self.power * multiplier, log)
            player1.hp += damage
            return True
        # if the card is nature, apply vines
        elif self.rune == Rune.NATURE:
            player2.vines += self.power * multiplier
            player2.take_damage(self.rune, 1 * multiplier, log)
            return True
        # if the card is fire, apply burning
        elif self.rune == Rune.FIRE:
            player2.take_damage(self.rune, self.power * multiplier, log)
            player2.burn = self.power * multiplier
            return True
        # if the card is water, hit 1-4 players
        elif self.rune == Rune.WATER:
            player1.burn = 0 # let players put out their burn with a water card
            players_dict = {i:players[i] for i in players if i != player1.sid }
            players_ = random.sample(list(players_dict.values()), min(random.randint(1,4), len(players_dict))) 
            for player_ in players_:
                if player_.sid != player1.sid:
                    player_.take_damage(self.rune, self.power * multiplier, log)
            return True
        # if the card is arcane, ignore shield
        elif self.rune == Rune.ARCANE:
            player2.take_damage(self.rune, self.power * multiplier, log)
            return True
        elif self.rune == Rune.WIND:
            player2.take_damage(self.rune, self.power * multiplier, log)
            return True