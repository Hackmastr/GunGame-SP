# ../gungame/core/events/__init__.py

"""GunGame custom event functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Site-Package
from path import Path

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH
from ..plugins.valid import valid_plugins


# =============================================================================
# >> CORE CUSTOM EVENT REGISTRATION
# =============================================================================
# Import the included events
for event_file in Path(__file__).parent.joinpath('included').files():
    if event_file.namebase != '__init__':
        import_module(
            'gungame.core.events.included.{module}'.format(
                module=event_file.namebase
            )
        )


# =============================================================================
# >> SUB-PLUGIN CUSTOM EVENT REGISTRATION
# =============================================================================
for plugin_name in valid_plugins.all:
    plugin_type = valid_plugins.get_plugin_type(plugin_name)
    if GUNGAME_PLUGINS_PATH.joinpath(
        plugin_type, plugin_name, 'custom_events.py',
    ).isfile():
        import_module(
            'gungame.plugins.{plugin_type}.{plugin_name}.custom_events'.format(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )
        )
