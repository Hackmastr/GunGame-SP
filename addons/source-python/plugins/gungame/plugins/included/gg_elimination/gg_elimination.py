# ../gungame/plugins/included/gg_elimination/gg_elimination.py

"""Plugin that respawns players when their killer is killed."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Collections
from collections import defaultdict

# Source.Python Imports
#   Events
from events import Event
#   Listeners
from listeners.tick import tick_delays
#   Players
from players.helpers import index_from_userid

# GunGame Imports
#   Status
from gungame.core.status import GunGameStatus
from gungame.core.status import GunGameRoundStatus
#   Messages
from gungame.core.messages import message_manager
#   Players
from gungame.core.players.dictionary import player_dictionary


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_eliminated_players = defaultdict(set)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _player_death(game_event):
    """Respawn any players the victim killed."""
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    victim = player_dictionary[game_event['userid']]
    tick_delays.delay(0, _respawn_victims, victim.userid)
    attacker = game_event['attacker']
    if attacker in (victim.userid, 0):
        tick_delays.delay(5, _respawn_player, victim.userid)
        victim.chat_message('Elimination_Respawn_Suicide')
        return
    killer = player_dictionary[attacker]
    if victim.team == killer.team:
        tick_delays.delay(5, _respawn_player, victim.userid)
        victim.chat_message('Elimination_Respawn_TeamKill')
        return
    # TODO: Test reconnecting to see if players are not respawned
    _eliminated_players[killer.userid].add(victim.userid)
    victim.chat_message(
        'Elimination_Respawn_Attacker', killer.index, attacker=killer)


@Event('round_start')
def _round_start(game_event):
    """Send the elimination info message."""
    message_manager.chat_message('Elimination_RoundInfo')


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _respawn_victims(userid):
    """Respawn all victim's of the given userid."""
    victims = _eliminated_players.pop(userid, None)
    if not victims:
        return
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    players = set()
    for victim in victims:
        if index_from_userid(victim, False) is not None:
            player = player_dictionary[victim]
            if player.team == 1:
                continue
            players.add(player.name)
            player.respawn()
    if players:
        message_manager.chat_message(
            'Elimination_Respawning', player.index,
            player='\x01, \x03'.join(sorted(players)))


def _respawn_player(userid):
    """Respawn the given userid after validation."""
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    if index_from_userid(userid, False) is not None:
        player_dictionary[userid].respawn()
