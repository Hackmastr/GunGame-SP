# ../gungame/core/teams.py

"""Provides team data."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from filters.entities import EntityIter
from players.teams import team_managers, teams_by_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'team_names',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
team_names = dict()

for _class_name in team_managers:
    for _entity in EntityIter(_class_name):
        if teams_by_number.get(_entity.team, 'un') not in ('un', 'spec'):
            team_names[_entity.team] = _entity.team_name