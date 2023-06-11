import random
from game_objects import Card, Dragon, Player
from game_logs import GameLogs
from enums import Rune, RUNES, CardType, DragonType
import Config

class Shop:
    def __init__(self, config: Config, data=None, ):
        self.items = []
        self.config = config
        self.data = data

    def cost_after_affinity(self, player: Player, item_idx: int):
        """
        return dict containing the cost of each rune with a value of 0 or the amount left over after affinities
        """
        item_cost = self.items[item_idx]["cost"]
        return {rune:max(0, int(item_cost[rune]) - int(player.affinities[rune])) for rune in item_cost}

    def can_afford(self, player: Player, item_idx: int):
        """
        player: an instance of the Player object
        item_idx: an index of an item in the shop
        return true if all of the dict.values = 0 in the total_cost dict
        """
        item_cost = self.items[item_idx]["cost"]
        total_cost = {rune:max(0, int(item_cost[rune]) - int(player.affinities[rune]) - int(player.runes[rune])) for rune in item_cost}

        return all([cost==0 for cost in total_cost.values()])

    def buy(self, player: Player, item_idx: int):
        pass

class DragonShop(Shop):
    def __init__(self, config, data=None):
        super().__init__(config, data)
        # Handle passing in JSON data from dynamodb
        if self.data is not None:
            self.items = [
                {
                    "dragon": Dragon(
                        runes=[Rune[rune] for rune in item['dragon']['runes']],
                        type=DragonType[item['dragon']['type']]), # turn the type e.g. "FIRE" into the Enum: DragonType.FIRE
                    "cost": item['cost']
                }
                for item in self.data
            ]
        else:
            self._generate_dragons()

    def _generate_dragons(self):
        sample = [
            {"dragon": Dragon(type=DragonType.CLOUD, runes=[Rune.WIND, Rune.WATER]),"cost": {Rune.WIND: 20, Rune.WATER: 20}},
            {"dragon": Dragon(type=DragonType.CRYSTAL, runes=[Rune.EARTH, Rune.ARCANE]), "cost": {Rune.EARTH: 20, Rune.ARCANE: 20}},
            {"dragon": Dragon(type=DragonType.DEEPSEA, runes=[Rune.WATER, Rune.DARK]), "cost": {Rune.WATER: 20, Rune.DARK: 20}},
            {"dragon": Dragon(type=DragonType.DUST, runes=[Rune.EARTH, Rune.WIND]), "cost": {Rune.EARTH: 20, Rune.WIND: 20}},
            {"dragon": Dragon(type=DragonType.LAVA, runes=[Rune.FIRE, Rune.EARTH]), "cost": {Rune.FIRE: 20, Rune.EARTH: 20}},
            {"dragon": Dragon(type=DragonType.LUNAR, runes=[Rune.SOLAR, Rune.DARK]), "cost": {Rune.SOLAR: 20, Rune.DARK: 20}},
            {"dragon": Dragon(type=DragonType.MUD, runes=[Rune.WATER, Rune.EARTH]), "cost": {Rune.WATER: 20, Rune.EARTH: 20}},
            {"dragon": Dragon(type=DragonType.NOVA, runes=[Rune.FIRE, Rune.SOLAR]), "cost": {Rune.FIRE: 20, Rune.SOLAR: 20}},
            {"dragon": Dragon(type=DragonType.STEAM, runes=[Rune.FIRE, Rune.WATER]), "cost": {Rune.FIRE: 20, Rune.WATER: 20}},
            {"dragon": Dragon(type=DragonType.STELLAR, runes=[Rune.SOLAR, Rune.WIND]), "cost": {Rune.SOLAR: 20, Rune.WIND: 20}},
            {"dragon": Dragon(type=DragonType.SWAMP, runes=[Rune.WATER, Rune.NATURE]), "cost": {Rune.WATER: 20, Rune.NATURE: 20}},
            {"dragon": Dragon(type=DragonType.THORN, runes=[Rune.NATURE, Rune.ARCANE]), "cost": {Rune.NATURE: 20, Rune.ARCANE: 20}},
            {"dragon": Dragon(type=DragonType.VOID, runes=[Rune.ARCANE, Rune.DARK]), "cost": {Rune.ARCANE: 20, Rune.DARK: 20}}
        ]
        # pick between 0 and length of the dragons that exist
        amount_to_gen = min(len(sample), max(0, self.config.dragons_in_shop)) 
        self.items = random.sample(sample, amount_to_gen)

    def buy(self, player: Player, item_idx):
        if self.can_afford(player, item_idx):
            for key, value in self.cost_after_affinity(player, item_idx).items():
                player.runes[key] -= value
            player.dragons.append(self.items[item_idx]["dragon"])
            self.items.pop(item_idx)
            return True
        return False
    
    def __dict__(self):
        dragons = []
        for dragon in self.items:
            dicify_dragon_obj = dragon['dragon'].__dict__()
            cost = { key.value: val for key, val in dragon['cost'].items() }
            dragons.append({'dragon': dicify_dragon_obj, 'cost': cost})
        return {
            "dragons": dragons
        }

class CardShop(Shop):
    def __init__(self, config, data=None):
        super().__init__(config, data)
        # Handle passing in JSON data from dynamodb
        if self.data is not None:
            self.items = [
                {
                    "card": Card(
                        rune=Rune[item['card']['rune']],
                        type=CardType[item['card']['type']],
                        affinity=item['card']['affinity'],
                        power=item['card']['power']), 
                    "cost": item['cost']
                } for item in self.data
            ]

        cards_in_shop = max(1, self.config.cards_in_shop)
        while len(self.items) < cards_in_shop:
            self._generate_card()

    def cycle(self):
        # generate a new card and put it on top
        self._generate_card()
        # pop off oldest card
        self.items.pop(self.config.cards_in_shop)

        # self.items = [card] + self.items

    def _generate_card(self):
        """
        returns a new legendary card and its cost as a tuple
        does not work for crafting basic cards
        """

        cost, total_cost = self._generate_cost()

        # roll the card power
        max_power = min(round(total_cost / 2), self.config.leg_max_power)
        min_power = max(round(total_cost / 4.5), self.config.leg_min_power)
        power = random.randint(min_power, max_power)

        # roll the type
        card_type = random.choice([CardType.ATTACK, CardType.SHIELD])

        # roll the affinity value 
        max_affinity = min(round(total_cost / 1.5), self.config.leg_max_affinity)
        max_affinity = max(max_affinity, self.config.leg_min_affinity)
        
        min_affinity = min(round(total_cost / 3), self.config.leg_max_affinity)
        min_affinity = max(min_affinity, self.config.leg_min_affinity)
        affinity = max(0, random.randint(min_affinity,max_affinity))
        
        # roll the element
        element = random.choices(list(cost.keys()), weights=list(cost.values()))[0]
        
        # make the card
        card = Card(element, card_type, affinity, power)
        
        # add card to top of shop list
        self.items.insert(0, {"card": card, "cost": cost})

    def _generate_cost(self):
        """
        returns a cost dict {"fire": 2, "water": 4} for legendary cards
        """
        # roll the total cost
        cost = {}
        total_cost = max(random.randint(self.config.leg_min_total_cost, self.config.leg_max_total_cost), 0)
        i = total_cost
        element = random.choice(list(Rune))                 # reroll element
        # iterate and distribute the runes to elements
        while i > 0:
            # roll 1/3 to change to a new element
            if random.randint(1,3) == 1:
                element = random.choice(list(Rune))         # reroll element
            # make sure you're not using an element that has exceeded its cap
            while cost.get(element, 0) >= self.config.leg_single_rune_max_cost:
                element = random.choice(list(Rune))         # reroll element
            
             # add 1 to the element cost
            cost[element] = cost.get(element, 0) + 1
            i-=1

        return cost, total_cost

    def buy(self, player, item_idx, log: GameLogs=None):
        """
        player: an instance of the Player object
        item_idx: index of the item in the shop
        log: the game log object instantiated in opulence.py
        """
        if self.can_afford(player, item_idx):
            for rune, cost in self.cost_after_affinity(player, item_idx).items():
                player.runes[rune] -= cost
            log.buy_card_log(player.display_name, self.items[item_idx]['card'])
            player.cards.append(self.items[item_idx])
            
            # remove card at index
            self.items.pop(item_idx)
            # generate a new card to the top (index 0)
            self._generate_card()
            return True
        return False

    def __dict__(self):
        # return only the card objects
        
        cards = []
        for card in self.items:
            dicify_card_obj = card['card'].__dict__()
            cost = { key.value: val for key, val in card['cost'].items() }
            cards.append({'card': dicify_card_obj, 'cost': cost})
        
        return {
            "cards": cards,
        }


class BasicCardShop(Shop):
    def __init__(self, config, data=None):
        super().__init__(config, data)
    
    def _generate_card(self, element1, element2):
        # basic cards do not populate a shop like the legendary cards do. Instead they're generated on the fly 
        # for the cost of 2 runes * 2 elements (4 runes total) | this method requires you to specify which 2 elements

        affinity = random.randint(2, 4)

        power = random.choices([1, 2, 3, 4, 5, 6], weights=[400, 500, 300, 50, 5, 1])
        power = power[0]

        card_type = random.choice([CardType.ATTACK, CardType.SHIELD])

        # force 1/3 of basic cards to be mundane
        if random.randint(1, 3) == 1:

            card_type = CardType.MUNDANE
            affinity += 2
            power = 0
        
        element = random.choice([element1, element2])

        return {'card': Card(element, card_type, affinity, power)}

    def cost_after_affinity(self, player: Player, item_cost: dict):
        """
        return dict containing runes with a value of 0 or the amount left over after affinities
        """
        return {rune:max(0, int(item_cost[rune]) - int(player.affinities[rune])) for rune in item_cost}

    def can_afford(self, player: Player, item_cost: dict):
        """
        player: an instance of the Player object
        item_idx: an index of an item in the shop
        return true if all of the dict.values = 0 in the dict returned from cost_after_affinity()
        """
        total_cost = {rune:max(0, int(item_cost[rune]) - int(player.affinities[rune]) - int(player.runes[rune])) for rune in item_cost}

        return all([cost==0 for cost in total_cost.values()])

    def buy(self, player, element1, element2, log: GameLogs=None):
        """
        player: an instance of the Player object
        elements 1&2: specified elements to spend to craft a basic card
        """
        if self.can_afford(player, {element1: 2, element2: 2}):
            for rune, cost in self.cost_after_affinity(player, {element1: 2, element2: 2}).items():
                player.runes[rune] -= cost
            card = self._generate_card(element1, element2)
            log.craft_card_log(player.display_name, card['card'], element1, element2)
            player.cards.append(card)
            return True
        return False