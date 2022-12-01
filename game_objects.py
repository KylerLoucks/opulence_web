import random
import json
import rune
import card_types
import dragon_types
class Shield:
    def __init__(self, rune: rune=None, power=0):
        self.rune = rune
        self.power = power

    def block(self, element: str, power, log, super_effective_multiplier=2.0):
        """
        - param element: the damage type the shield is blocking incoming damage from
        TODO: super_effective_multiplier should come from config?
        """
        multiplier = 1.0
        pairs = {
            (rune.FIRE, rune.NATURE),
            (rune.WATER, rune.FIRE),
            (rune.EARTH, rune.WIND),
            (rune.NATURE, rune.EARTH),
            (rune.SOLAR, rune.SOLAR),
            (rune.DARK, rune.DARK),
            (rune.WIND, rune.WATER)
        }

        # arcane goes through shields
        if element == rune.ARCANE:
            return power

        if element == rune.WIND:
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
            "rune": self.rune,
            "power": self.power
        }

class Player:
    def __init__(self, sid: str, hp=10, shield: Shield=None, name: str=None):
        self.sid = sid
        self.hp = hp
        self.shield = Shield() if shield == None else shield
        self.runes = {rune:0 for rune in rune.RUNES}
        self.affinities = {rune:0 for rune in rune.RUNES}
        self.cards = []
        self.dragons = []
        self.isDead = False
        self.display_name = sid if name == None else name
        # status effects, handled elsewhere
        self.vines = 0
        self.burn = 0

    def update_affinities(self):
        # updated every time a card is bought/played
        self.affinities = {rune:0 for rune in rune.RUNES}
        for card in self.cards:
            self.affinities[card['card'].rune] += card['card'].affinity

    def take_damage(self, rune, power, log):
        """
        rune: str The element type e.g. (rune.FIRE)
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

    def get_dragon_multiplier(self, rune_type: rune=None):
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
            "display_name": self.display_name
        }

    # used for testing
    def add_card(self):
        """
        Add a new Card object to the players cards (list)
        """
        self.cards.append({'card': Card(rune.EARTH, card_types.SHIELD, 5, 15)})
        self.update_affinities()
   
    # used for testing
    def add_dragon(self):
        """
        Add a new Dragon object to the players dragons (list)
        """
        self.dragons.append(Dragon(type=dragon_types.VOID, runes=[rune.ARCANE, rune.DARK]))
        self.dragons.append(Dragon(type=dragon_types.STEAM, runes=[rune.ARCANE, rune.DARK]))

    # for testing
    def set_runes(self):
        self.runes = {rune:20 for rune in rune.RUNES}

    def __str__(self):
        return json.dumps(self.__dict__())



class Dragon:
    """
    Dragon objects that can be held by a player
    - param type: The card type e.g. (dragon_types.SOLAR)
    - param runes: The two runes associated with the dragon
    """
    def __init__(self, type: dragon_types, runes: list):
        self.type = type
        self.runes = runes
    
    def __dict__(self):
        return {
            "type": self.type,
            "runes": self.runes,
        }


class Card:
    """
    Card objects that can be held by a player
    - param rune: The element the card is e.g. (rune.FIRE) 
    - param type: The card type e.g. (card_types.ATTACK)
    - param affinity: The amount the card is worth in affinity
    - param power: the base amount the card does in damage/shield before modifiers
    """
    def __init__(self, rune: rune, type: card_types, affinity, power):
        self.rune = rune
        self.type = type
        self.affinity = affinity
        self.power = power

    def __dict__(self):
        return {
            "rune": self.rune,
            "type": self.type,
            "affinity": self.affinity,
            "power": self.power
        }

    def activate(self, player1: Player, player2, players: dict, log):
        """
        player: instance of Player object for the player of the card
        players: dict of the Player objects
        """
        if self.type == card_types.MUNDANE:
            return False
        elif self.type == card_types.ATTACK:
            return self._activate_attack(player1, player2, players, log)
        elif self.type == card_types.SHIELD:
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
            fire_bonus = 4.0 if self.rune == rune.FIRE else 1.0         # fire does 4x damage to vines
            vines_left_over = player1.vines - self.power * multiplier * fire_bonus
            player1.vines = max(0, vines_left_over)
            self.power = -min(0, vines_left_over)//fire_bonus

        # if the card is earth, roll for crit chance
        if self.rune == rune.EARTH:
            # TODO: hard-coded earth crit chance should come from config?
            crit = random.random() < 0.25
            self.power = self.power*3 if crit else self.power
            if crit:
                print(f"Earth card that was played * CRIT * causing the power to be: {self.power}")

            player2.take_damage(self.rune, self.power * multiplier, log)
            return True

        # if the card is solar, do damage to everyone
        elif self.rune == rune.SOLAR:
            for player_ in players.values():
                player_.take_damage(self.rune, self.power * multiplier, log)
            return True
        # if the card is dark, heal the player
        elif self.rune == rune.DARK:
            damage = player2.take_damage(self.rune, self.power * multiplier, log)
            player1.hp += damage
            return True
        # if the card is nature, apply vines
        elif self.rune == rune.NATURE:
            player2.vines += self.power * multiplier
            player2.take_damage(self.rune, 1 * multiplier, log)
            return True
        # if the card is fire, apply burning
        elif self.rune == rune.FIRE:
            player2.take_damage(self.rune, self.power * multiplier, log)
            player2.burn = self.power * multiplier
            return True
        # if the card is water, hit 1-4 players
        elif self.rune == rune.WATER:
            player1.burn = 0 # let players put out their burn with a water card
            players_dict = {i:players[i] for i in players if i != player1.sid }
            players_ = random.sample(list(players_dict.values()), min(random.randint(1,4), len(players_dict))) 
            for player_ in players_:
                if player_.sid != player1.sid:
                    player_.take_damage(self.rune, self.power * multiplier, log)
            return True
        # if the card is arcane, ignore shield
        elif self.rune == rune.ARCANE:
            player2.take_damage(self.rune, self.power * multiplier, log)
            return True
        elif self.rune == rune.WIND:
            player2.take_damage(self.rune, self.power * multiplier, log)
            return True