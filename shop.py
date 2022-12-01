import random

from game_objects import Card, Dragon, Player
import rune
import card_types
import dragon_types
from game_logs import GameLogs

class Shop:
    def __init__(self, config):
        self.items = []
        self.config = config

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generate_dragons()

    def _generate_dragons(self):
        sample = [
            {"dragon": Dragon(type=dragon_types.CLOUD, runes=[rune.WIND, rune.WATER]),"cost": {rune.WIND: 20, rune.WATER: 20}},
            {"dragon": Dragon(type=dragon_types.CRYSTAL, runes=[rune.EARTH, rune.ARCANE]), "cost": {rune.EARTH: 20, rune.ARCANE: 20}},
            {"dragon": Dragon(type=dragon_types.DEEPSEA, runes=[rune.WATER, rune.DARK]), "cost": {rune.WATER: 20, rune.DARK: 20}},
            {"dragon": Dragon(type=dragon_types.DUST, runes=[rune.EARTH, rune.WIND]), "cost": {rune.EARTH: 20, rune.WIND: 20}},
            {"dragon": Dragon(type=dragon_types.LAVA, runes=[rune.FIRE, rune.EARTH]), "cost": {rune.FIRE: 20, rune.EARTH: 20}},
            {"dragon": Dragon(type=dragon_types.LUNAR, runes=[rune.SOLAR, rune.DARK]), "cost": {rune.SOLAR: 20, rune.DARK: 20}},
            {"dragon": Dragon(type=dragon_types.MUD, runes=[rune.WATER, rune.EARTH]), "cost": {rune.WATER: 20, rune.EARTH: 20}},
            {"dragon": Dragon(type=dragon_types.NOVA, runes=[rune.FIRE, rune.SOLAR]), "cost": {rune.FIRE: 20, rune.SOLAR: 20}},
            {"dragon": Dragon(type=dragon_types.STEAM, runes=[rune.FIRE, rune.WATER]), "cost": {rune.FIRE: 20, rune.WATER: 20}},
            {"dragon": Dragon(type=dragon_types.STELLAR, runes=[rune.SOLAR, rune.WIND]), "cost": {rune.SOLAR: 20, rune.WIND: 20}},
            {"dragon": Dragon(type=dragon_types.SWAMP, runes=[rune.WATER, rune.NATURE]), "cost": {rune.WATER: 20, rune.NATURE: 20}},
            {"dragon": Dragon(type=dragon_types.THORN, runes=[rune.NATURE, rune.ARCANE]), "cost": {rune.NATURE: 20, rune.ARCANE: 20}},
            {"dragon": Dragon(type=dragon_types.VOID, runes=[rune.ARCANE, rune.DARK]), "cost": {rune.ARCANE: 20, rune.DARK: 20}}
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
            dragons.append({'dragon': dicify_dragon_obj, 'cost': dragon['cost']})
        
        return {
            "dragons": dragons
        }

class CardShop(Shop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        card_type = random.choice([card_types.ATTACK, card_types.SHIELD])

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
        element = random.choice(rune.RUNES)                 # reroll element
        # iterate and distribute the runes to elements
        while i > 0:
            # roll 1/3 to change to a new element
            if random.randint(1,3) == 1:
                element = random.choice(rune.RUNES)         # reroll element
            # make sure you're not using an element that has exceeded its cap
            while cost.get(element, 0) >= self.config.leg_single_rune_max_cost:
                element = random.choice(rune.RUNES)         # reroll element
            
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
            cards.append({'card': dicify_card_obj, 'cost': card['cost']})
        
        # cards = deepcopy(self.items) #deepcopy
        # for index, card in enumerate(cards):
        #     cards[index]['card'] = card['card'].__dict__()
        
        return {
            "cards": cards,
        }


class BasicCardShop(Shop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _generate_card(self, element1, element2):
        # basic cards do not populate a shop like the legendary cards do. Instead they're generated on the fly 
        # for the cost of 2 runes * 2 elements (4 runes total) | this method requires you to specify which 2 elements

        affinity = random.randint(2, 4)

        power = random.choices([1, 2, 3, 4, 5, 6], weights=[400, 500, 300, 50, 5, 1])
        power = power[0]

        card_type = random.choice([card_types.ATTACK, card_types.SHIELD])

        # force 1/3 of basic cards to be mundane
        if random.randint(1, 3) == 1:

            card_type = card_types.MUNDANE
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