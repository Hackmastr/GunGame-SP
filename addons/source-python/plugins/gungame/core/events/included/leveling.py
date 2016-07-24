# ../gungame/core/events/included/leveling.py

"""Leveling based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ByteVariable, ShortVariable, StringVariable

# GunGame
from ..resource import GGResourceFile


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_LevelDown',
    'GG_LevelUp',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_LevelUp(CustomEvent):
    """Called when a player levels up."""

    attacker = leveler = ShortVariable(
        'The userid of the player that leveled up'
    )
    userid = victim = ShortVariable(
        'The userid of the victim that caused the levelup'
    )
    old_level = ByteVariable('The old level of the player that leveled up')
    new_level = ByteVariable('The new level of the player that leveled up')
    reason = StringVariable('The reason for the levelup')


class GG_LevelDown(CustomEvent):
    """Called when a player loses a level."""

    userid = leveler = ShortVariable(
        'The userid of the player that leveled down'
    )
    attacker = ShortVariable(
        'The userid of the player that caused the level down'
    )
    old_level = ByteVariable('The old level of the player that leveled down')
    new_level = ByteVariable('The new level of the player that leveled down')
    reason = StringVariable('The reason for the leveldown')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile('leveling', GG_LevelUp, GG_LevelDown)
