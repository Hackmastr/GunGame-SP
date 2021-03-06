# ../gungame/plugins/included/gg_dissolver/configuration.py

"""Creates the gg_disable_objectives configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities.constants import DissolveType

# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'dissolver_delay',
    'dissolver_type',
    'magnitude',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('type') as dissolver_type:

        for _name in DissolveType.__members__:
            dissolver_type.Options.append(
                '{value} = {name}'.format(
                    value=getattr(DissolveType, _name).real,
                    name=_name,
                )
            )

        _num_dissolve_types = len(DissolveType.__members__)
        dissolver_type.add_text(
            random=_num_dissolve_types,
            remove=_num_dissolve_types + 1,
        )

    with _config.cvar('magnitude', 2) as magnitude:
        magnitude.add_text()

    with _config.cvar('delay') as dissolver_delay:
        dissolver_delay.add_text()
