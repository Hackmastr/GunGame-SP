# ../gungame/core/menus/_rankings.py

"""Provides the menu base for winners and rank."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu

# GunGame
from . import _menu_strings
from ._options import ListOption
from ..players.database import winners_database


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_winners_menu(player):
    """Return a sorted menu of all winners."""
    menu = PagedMenu(title=_menu_strings['Winners:Title'])
    if not winners_database:
        menu.description = _menu_strings['Winners:None']
        return menu

    winners = sorted(
        winners_database,
        key=lambda unique_id: (
            winners_database[unique_id].wins,
            -winners_database[unique_id].time_stamp,
        ),
        reverse=True,
    )
    for rank, unique_id in enumerate(winners, 1):
        instance = winners_database[unique_id]
        menu.append(
            ListOption(
                rank,
                '{name} [{wins}]'.format(
                    name=instance.name,
                    wins=instance.wins
                ),
                unique_id,
                player.unique_id == unique_id,
                False,
            )
        )
    return menu
