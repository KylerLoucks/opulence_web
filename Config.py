class Config:
    def __init__(self,
            # user configs
            max_players = 8,
            runes_per_turn = 5,
            super_effective_multiplier = 2,
            cards_in_shop = 8,
            dragons_in_shop = 2,
            player_starting_health = 10,
            turn_timer = 10,
            #        global configs
            # leg means legendary
            leg_min_power = 4,                  # power = damage / shield potency (negative rounds to 0 on roll)
            leg_max_power = 20,         
            leg_min_affinity = 4,       
            leg_max_affinity = 10,
            leg_min_total_cost = 10,            # how many total runes will this card cost
            leg_max_total_cost = 22,
            leg_single_rune_max_cost = 28       # max runes in a single element this card can cost


            ):
        # user configs
        self.max_players = max_players
        self.runes_per_turn = runes_per_turn
        self.super_effective_multiplier = super_effective_multiplier
        self.cards_in_shop = cards_in_shop
        self.dragons_in_shop = dragons_in_shop
        self.player_starting_health = player_starting_health
        self.turn_timer = turn_timer
        # global configs
        self.leg_min_power = leg_min_power
        self.leg_max_power = leg_max_power
        self.leg_min_affinity = leg_min_affinity
        self.leg_max_affinity = leg_max_affinity
        self.leg_min_total_cost = leg_min_total_cost
        self.leg_max_total_cost = leg_max_total_cost
        self.leg_single_rune_max_cost = leg_single_rune_max_cost
        

