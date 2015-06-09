# ../gungame/core/leaders.py

"""Tracks the leader and calls leader based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from cvars import ConVar
from filters.players import PlayerIter

from gungame.core.events.included.leaders import GG_Leader_Disconnect
from gungame.core.events.included.leaders import GG_Leader_LostLevel
from gungame.core.events.included.leaders import GG_New_Leader
from gungame.core.events.included.leaders import GG_Tied_Leader
from gungame.core.messages import message_manager
from gungame.core.players.dictionary import player_dictionary


# =============================================================================
# >> CLASSES
# =============================================================================
class _LeaderManager(dict):

    """Class used to track leaders."""

    def __init__(self):
        """Add all current players to the dictionary."""
        super(_LeaderManager, self).__init__()
        for userid in PlayerIter(return_types='userid'):
            self[userid] = player_dictionary[userid].level

    @property
    def leader_level(self):
        """Return the level of the leader."""
        return max(self.values() or [1])

    @property
    def current_leaders(self):
        """Return a list of current leaders."""
        level = self.leader_level
        if level == 1:
            return None
        return [userid for userid in self if self[userid] == level]

    def is_leading(self, userid):
        """Return whether the given player is a leader or not."""
        return self[userid] == self.leader_level != 1

    def add_player(self, userid):
        """Add the player to the dictionary."""
        self[userid] = player_dictionary[userid].level

    def player_levelup(self, userid):
        """Set the player's level and see if the leaders changed."""
        player_level = player_dictionary[userid].level
        if player_level < self.leader_level:
            return
        old_leaders = self._get_leader_string()
        old_level = self.leader_level
        player = player_dictionary[userid]
        self[userid] = player.level
        new_leaders = self._get_leader_string()
        new_level = self.leader_level
        count = len(self.current_leaders)
        if count > 1:
            with GG_Tied_Leader() as event:
                event.userid = event.leveler = userid
                event.old_leaders = old_leaders
                event.leaders = new_leaders
                event.leader_level = new_level
            message = 'Leader_Tied_{0}'.format(
                'Singular' if count == 2 else 'Plural')
            self._send_leader_message(
                message, player.index, count=count,
                name=player.name, level=new_level)
        else:
            with GG_New_Leader() as event:
                event.userid = event.leveler = userid
                event.old_leaders = old_leaders
                event.old_level = old_level
                event.leaders = new_leaders
                event.leader_level = new_level
            self._send_leader_message(
                'Leader_New', player.index, name=player.name, level=new_level)

    def player_leveldown(self, userid):
        """Set the player's level and see if the leaders changed."""
        if not self.is_leading(userid):
            self[userid] = player_dictionary[userid].level
            return
        old_leaders = self._get_leader_string()
        old_level = self[userid]
        self[userid] = player_dictionary[userid].level
        new_level = self.leader_level
        with GG_Leader_LostLevel() as event:
            event.userid = event.leveler = userid
            event.old_leaders = old_leaders
            event.old_level = old_level
            event.leaders = self._get_leader_string()
            event.leader_level = new_level
        self._check_new_leaders(userid)

    def check_disconnect(self, userid):
        """Remove the player and see if the leaders changed."""
        if not self.is_leading(userid):
            del self[userid]
            return
        old_leaders = self._get_leader_string()
        old_level = self[userid]
        del self[userid]
        with GG_Leader_Disconnect() as event:
            event.userid = userid
            event.old_leaders = old_leaders
            event.old_level = old_level
            event.leaders = self._get_leader_string()
            event.leader_level = self.leader_level
        self._check_new_leaders(userid)

    def _check_new_leaders(self, userid):
        """Check to see if the leaders changed and send messages."""
        current = self.current_leaders
        if current is None or (len(current) == 1 and userid in current):
            return
        level = self.leader_level
        if len(current) == 1:
            player = player_dictionary[current[0]]
            self._send_leader_message(
                'Leader_New', player.index, name=player.name, level=level)
        else:
            names = [player_dictionary[player].name for player in current]
            self._send_leader_message(
                'Leader_New_Plural', names=names, level=level)

    def _get_leader_string(self):
        """Return a string of leader userids."""
        leaders = self.current_leaders
        if leaders is None:
            return ''
        return ','.join(map(str, leaders))

    @staticmethod
    def _send_leader_message(message, index=0, **tokens):
        """Send the given message to players."""
        if ConVar('gg_leader_messages').get_int():
            message_manager.chat_message(
                index=index, message=message, **tokens)

leader_manager = _LeaderManager()
