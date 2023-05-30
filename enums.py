from enum import Enum


class CardType(Enum):
    SHIELD = "SHIELD"    # absorbs damage
    ATTACK = "ATTACK"   # deals damage
    MUNDANE = "MUNDANE"   # only grants affinity

TYPES = [card.value for card in CardType]


class DragonType(Enum):
    CLOUD = "CLOUD"
    CRYSTAL = "CRYSTAL"
    DEEPSEA = "DEEP-SEA"
    DUST = "DUST"
    LAVA = "LAVA"
    LUNAR = "LUNAR"
    MUD = "MUD"
    NOVA = "NOVA"
    SMOKE = "SMOKE"
    STEAM = "STEAM"
    STELLAR = "STELLAR"
    SWAMP = "SWAMP"
    THORN = "THORN"
    VOID = "VOID"

DRAGONS = [dragon.value for dragon in DragonType]

class Rune(Enum):
    FIRE = "FIRE"    # hits twice, weak to water
    WATER = "WATER"   # hits 1-4 people?
    EARTH = "EARTH"   # 25% chance to crit
    WIND = "WIND"    # 2x damage to shields, weak to earth
    NATURE = "NATURE" # vines meme, weak to fire (?)
    DARK = "DARK"    # lifesteal
    SOLAR = "SOLAR"  # hits everything, weak to solar
    ARCANE = "ARCANE"  # ignores shields

RUNES = [rune.value for rune in Rune]