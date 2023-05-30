from enums import Rune
from game_objects import Player, Card

class GameLogs:
    def __init__(self) -> None:
        self.logs = []
        self.damage_to_shield = 0
        self.damage_to_health = 0
        self.player_died = False
        self.shield_destroyed = False
        self.took_burn_dmg = False
        self.took_poison_dmg = False
        self.super_effective = False
        self.new_death = None
        self.winner = None



        self.vines = 0


    def winner_log(self, sid: str=None):
        """
        Appends to the logs the name of the player who won the game
        """
        if sid == None:
            log_msg = f":skull: GAME OVER! Everyone DIED :skull: There are no winners here..."
        else:
            log_msg = f":skull: GAME OVER! :skull: User: {sid} won the game!"
        self.logs.append(log_msg)

    def create_game_log(self, sid, gameID):
        """
        Appends to the logs that an Opulence game object was created
        """
        log_msg = f"User: {sid} created lobby with a gameID of: {gameID}."
        self.logs.append(log_msg)

    def start_game_log(self, sid, sid2):
        """
        - param sid: the sid of the player who started the game
        - param sid2: the sid of the player whos turn it is when the game starts
        """
        log_msg = f"User: {sid} started the game! It's {sid2}'s turn"
        self.logs.append(log_msg)

    def join_game_log(self, sid):
        """
        - param sid: the sid of the player who joined the game
        """
        log_msg = f"User: {sid} joined the game!"
        self.logs.append(log_msg)

    def leave_game_log(self, sid, while_started=False, disconnected=False):
        """
        - param sid: the sid of the player who left the game
        """
        if disconnected and while_started:
            log_msg = f"User: {sid} deleted their system32 folder WHILE IT WAS THEIR TURN."
        elif disconnected:
            log_msg = f"User: {sid} deleted their system32 folder."
        elif while_started:
            log_msg = f"User: {sid} left the game WHILE IT WAS THEIR TURN."
        else:
            log_msg = f"User: {sid} left the game..."
        self.logs.append(log_msg)

    def take_rune_log(self, sid, element: str):
        parsed = self._parse_rune(element)
        log_msg = f"{sid} took x1 {parsed} rune."
        self.logs.append(log_msg)
    
    def buy_card_log(self, sid, card: Card):
        parsed = self._parse_rune(card.rune.value)
        log_msg = f"{sid} bought a x{card.power} power {card.type} card worth x{card.affinity} {parsed} affinity."
        self.logs.append(log_msg)
    
    def craft_card_log(self, sid, card: Card, element1, element2):
        parsed = self._parse_rune(card.rune.value)
        log_msg = f"{sid} crafted a x{card.power} power {card.type} card worth x{card.affinity} {parsed} affinity."
        self.logs.append(log_msg)
    
    def play_card_log(self, card: Card, player1: Player, player2: Player=None):
        parsed = self._parse_rune(card.rune.value)
        log_msg = f"{player1.display_name} played a x{card.power} power {card.type} card worth x{card.affinity} {parsed} affinity; granting them a {card.power} {parsed} SHIELD."
        
        if player2 is not None:
            log_msg = f"{player1.display_name} played a x{card.power} power {card.type} card worth x{card.affinity} {parsed} affinity on {player2.display_name}."

        # log the card type for notifications
        self.played_card = card.type

        self.logs.append(log_msg)

    def next_turn_log(self, sid):
        log_msg = f"It's {sid}'s turn"
        self.logs.append(log_msg)
    
    def player_took_damage_log(self, player: str, element: str):
        """
        - param player: the sid or name of the player who took damage
        - param element: the type of damage the player took (e.g. rune.FIRE)
        """
        element = self._parse_rune(element)
        if self.took_burn_dmg:
            if self.player_died:
                if self.damage_to_shield > 0:
                    log_msg = f"{player} took {self.damage_to_shield} :burn: damage to their shield and {self.damage_to_health} :burn: damage to their health, :skull: burning them to death. :skull:"
                    if self.super_effective:
                        log_msg = f"{player} took {self.damage_to_shield} * SUPER EFFECTIVE * :burn: damage to their shield and {self.damage_to_health} :burn: damage to their health, :skull: burning them to death. :skull:"
                log_msg = f"{player} took {self.damage_to_health} :burn: damage to their health, :skull: burning them to death. :skull:"
                self.new_death = "fire"
            elif self.damage_to_health > 0 and self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} :burn: damage to their shield and {self.damage_to_health} :burn: damage to their health."
                if self.super_effective:
                    log_msg = f"{player} took {self.damage_to_shield} * SUPER EFFECTIVE * :burn: damage to their shield and {self.damage_to_health} :burn: damage to their health."
            elif self.damage_to_health > 0:
                log_msg = f"{player} took {self.damage_to_health} :burn: damage to their health."
            elif self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} :burn: damage to their shield."
                if self.super_effective:
                    log_msg = f"{player} took {self.damage_to_shield} * SUPER EFFECTIVE * :burn: damage to their shield."
        
        elif self.took_poison_dmg:
            if self.player_died:
                if self.damage_to_shield > 0:
                    log_msg = f"{player} took {self.damage_to_shield} :poison: damage to their shield and {self.damage_to_health} :poison: damage to their health, :skull: poisoning them to death. :skull:"
                log_msg = f"{player} took x{self.damage_to_health} :poison: damage to their health, :skull: poisoning them to death. :skull:"
                self.new_death = "nature"
            elif self.damage_to_health > 0 and self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} :poison: damage to their shield and {self.damage_to_health} :poison: damage to their health."
            elif self.damage_to_health > 0:
                log_msg = f"{player} took {self.damage_to_health} :poison: damage to their health."
            elif self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} :poison: damage to their shield."
                if self.super_effective:
                    log_msg = f"{player} took {self.damage_to_shield} * SUPER EFFECTIVE * :poison: damage to their shield."
        
        elif self.player_died:
            if self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} {element} damage to their shield and {self.damage_to_health} {element} damage to their health, :skull: killing them. :skull:"
                if self.super_effective:
                    log_msg = f"{player} took {self.damage_to_shield} {element} * SUPER EFFECTIVE * damage to their shield and {self.damage_to_health} {element} damage to their health, :skull: killing them. :skull:"
            else:
                log_msg = f"{player} took {self.damage_to_health} {element} damage to their health, :skull: killing them. :skull:"
            self.new_death = element.replace(":", "")
        elif self.damage_to_health > 0 and self.damage_to_shield > 0:
                log_msg = f"{player} took {self.damage_to_shield} {element} damage to their shield and {self.damage_to_health} {element} damage to their health."
                if self.super_effective:
                    log_msg = f"{player} took {self.damage_to_shield} {element} * SUPER EFFECTIVE * damage to their shield and {self.damage_to_health} {element} damage to their health."
        elif self.damage_to_health > 0:
            log_msg = f"{player} took {self.damage_to_health} {element} damage to their health."
        elif self.damage_to_shield > 0:
            log_msg = f"{player} took {self.damage_to_shield} {element} damage to their shield."
            if self.super_effective:
                log_msg = f"{player} took {self.damage_to_shield} {element} * SUPER EFFECTIVE * damage to their shield."
        else:
            return

        self.logs.append(log_msg)

        # Reset stored information
        self.damage_to_health = 0
        self.damage_to_shield = 0
        self.player_died = False
        self.took_burn_dmg = False
        self.took_poison_dmg = False
        self.shield_destroyed = False
        self.super_effective = False


    def _parse_rune(self, element: str):
        """
        parses the rune string from e.g. "ARCANE" to ":arcane:"
        returns the appropriate emoji tag for the front-end
        """
        if element == Rune.ARCANE.value:
            return ":arcane:"
        elif element == Rune.DARK.value:
            return ":dark:"
        elif element == Rune.EARTH.value:
            return ":earth:"
        elif element == Rune.FIRE.value:
            return ":fire:"
        elif element == Rune.NATURE.value:
            return ":nature:"
        elif element == Rune.WATER.value:
            return ":water:"
        elif element == Rune.SOLAR.value:
            return ":solar:"
        elif element == Rune.WIND.value:
            return ":wind:"
        




