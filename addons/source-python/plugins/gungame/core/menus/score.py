# ../gungame/core/menus/score.py

"""Score menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu
from players.entity import Player

# GunGame
from . import menu_strings
from ._options import ListOption
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..teams import team_levels, team_names


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_score_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_score_menu(index):
    """Send the score menu to the player."""
    menu = PagedMenu(title=menu_strings['Score:Title'])
    player = Player(index)
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    elif gg_plugin_manager.is_team_game:
        for team in sorted(
            team_levels,
            key=lambda x: team_levels[x],
            reverse=True,
        ):
            menu.append(
                ListOption(
                    choice_index=team_levels[team],
                    text=team_names[team],
                    value=team,
                    highlight=team == player.team,
                    selectable=False,
                )
            )
    else:
        for userid in sorted(
            player_dictionary,
            key=lambda key: player_dictionary[key].level,
            reverse=True,
        ):
            current_player = player_dictionary[userid]
            menu.append(
                ListOption(
                    choice_index=current_player.level,
                    text=current_player.name,
                    value=current_player.unique_id,
                    highlight=current_player.unique_id == player.unique_id,
                    selectable=False,
                )
            )
    menu.send(index)
