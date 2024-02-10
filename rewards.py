
# rarities = ['common', 'uncommon', 'rare', 'very_rare', 'epic', 'legendary']

# baseline_probabilities = [0.1, 0.05, 0.03, 0.02, 0.01, 0.005]

# def roll_for_icon(crate_rarity):
#     # Multiply the weights by the index to raise the chance
#     new_probabilities = [prob + 0.001 * rarities.index(crate_rarity) for prob in baseline_probabilities] 
#     item_rarity = random.choices(rarities, new_probabilities)[0]
#     print(item_rarity)
#     print(new_probabilities)
#     # if the rarity rolled is lower than the crate rarity, set it to the crate rarity.
#     if rarities.index(item_rarity) < rarities.index(crate_rarity):
#         item_rarity = crate_rarity
#     return item_rarity

# print(roll_for_icon('uncommon'))


import random
from enums import RUNES, TYPES
from enum import Enum

class Rewards(Enum):
    common = ['t']
    uncommon = ['h']
    rare = ['u', '4', '5']
    very_rare = ['o']
    epic = ['p']
    legendary = ['e']


power_values = {
    'common': random.randint(1,2),
    'uncommon': random.randint(2,3),
    'rare': random.randint(3,4),
    'very_rare': random.randint(4,5),
    'epic': random.randint(5,6),
    'legendary': 6
}

afinity_values = {
    'common': random.randint(1,2),
    'uncommon': random.randint(3,4),
    'rare': random.randint(4,5),
    'very_rare': random.randint(5,6),
    'epic': random.randint(7,8),
    'legendary': 8
}

def give_item(rarity):

    if random.randint(1, 2) == 1:
        return {'card': generate_card(rarity)}
    
    # Grab a random icon from the icons list
    icon_list = rarity.value
    random_icon = icon_list[random.randint(0, len(icon_list) - 1)]
    return {'icon': random_icon}

def generate_card(rarity):
    
    # roll the card power
    power = power_values[rarity.name]

    # roll the type
    card_type = random.choice(TYPES)

    # roll the affinity value 
    affinity = afinity_values[rarity.name]
    if card_type == 'MUNDANE':
        power = 0
        affinity += random.randint(1,3)
        
    # roll the element
    element = random.choice(RUNES)[0]

    card = {'affinity': affinity, 'power': power, 'rune': element, 'type': card_type}
    return card

def open_crate(rarity=Rewards.common, n=1):
    # returns a list of loot you got from opening a crate

    while random.randint(1, 4) == 1 and rarity != Rewards.legendary:
        enum_index = list(Rewards).index(rarity)
        rarity = list(Rewards)[enum_index + 1]
    
    print(rarity)

    return give_item(rarity=rarity)
    # rewards.append(random.choice(crate_rewards[r]))