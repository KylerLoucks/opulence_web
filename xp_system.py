from game_objects import Player
import random

class XPSystem:
    def __init__(self) -> None:
        self.xp_multi = 50
        self.xp_additional = 325

    def calc_req_xp(self, player: Player):
        # This function takes a players level and 
        # returns how much xp in total is required to level up
        level = player.level
        return ((level * self.xp_multi) + self.xp_additional)
    
    def calc_xp_needed(self, player: Player):
        # Calculates xp needed to level up
        xp_needed = player.xp - self.calc_req_xp(player)
        return xp_needed
    
    def give_xp(self, player: Player, xp):
        # This function takes a player and an XP int and gives it to the user,
        # returning True if he levels up, or False if he doesn't
        prior_lvl = player.level
        current_lvl = player.level
        current_xp = player.xp
        current_xp += xp

        #check for levelup
        if current_xp >= self.calc_req_xp(player):
            #recursive levelup
            while current_xp >= self.calc_req_xp(player):
                current_xp -= self.calc_req_xp(player)
                current_lvl += 1

            # give loot crates for the level ups
            player.rewards['common_crates'] += (current_lvl - prior_lvl)
            return True
            
        else:
            return False
    
    def roll_key(self, xp):
        return random.random() < xp / 999