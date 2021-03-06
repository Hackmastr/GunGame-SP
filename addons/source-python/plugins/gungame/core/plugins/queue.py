# ../gungame/core/plugins/queue.py

"""Provides a plugin queue class that loads/unloads plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from listeners.tick import Delay

# GunGame
from ..events.included.plugins import GG_Plugin_Loaded
from ..plugins import gg_plugins_logger
from ..plugins.manager import gg_plugin_manager
from ..plugins.valid import plugin_requirements, valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_PluginQueue',
    'plugin_queue',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_queue_logger = gg_plugins_logger.queue


# =============================================================================
# >> CLASSES
# =============================================================================
class _PluginQueue(dict):
    """Plugin queue class used to load/unload plugins."""

    manager = gg_plugin_manager
    translations = manager.translations
    logger = gg_plugins_queue_logger
    prefix = None

    def __missing__(self, item):
        """Add the item to its queue and loop through queues after 1 tick."""
        if item not in ('load', 'unload', 'reload'):
            raise ValueError(
                'Invalid plugin type "{queue_name}"'.format(
                    queue_name=item,
                )
            )
        if not self:
            Delay(0, self._loop_through_queues)
        value = self[item] = set()
        return value

    def _loop_through_queues(self):
        """Loop through all queues to properly load/unload plugins."""
        if 'unload' in self:
            self._unload_plugins()
            del self['unload']
        if 'load' in self:
            self._load_plugins()
            del self['load']
        if 'reload' not in self:
            return
        self['load'] = set(self['reload'])
        del self['reload']

    def _unload_plugins(self):
        """Unload all plugins in the unload queue."""
        # Loop through all plugins to unload
        for plugin_name in self['unload']:

            if plugin_name in plugin_requirements:
                for other in plugin_requirements[plugin_name]:
                    if other in self.manager and other not in self['unload']:
                        warn(
                            'Plugin "{plugin_name}" is required by "{other}". '
                            'Please unload "{other}" or load {plugin_name} '
                            'again to avoid issues.'.format(
                                plugin_name=plugin_name,
                                other=other,
                            )
                        )

            # Unload the plugin
            del self.manager[plugin_name]

    def _load_plugins(self):
        """Load all plugins in the load queue."""
        # Loop through all plugins to load
        for plugin_name in self['load']:

            # Retrieve the plugin's type
            try:
                plugin_type = valid_plugins.get_plugin_type(plugin_name)
            except ValueError:
                warn(
                    'Plugin "{plugin_name}" is invalid.'.format(
                        plugin_name=plugin_name,
                    )
                )
                continue
            plugin_info = getattr(valid_plugins, plugin_type)[plugin_name].info

            # Check for conflicts
            if hasattr(plugin_info, 'conflicts'):
                conflict = False
                for other in plugin_info.conflicts:
                    if other in self.manager:
                        warn(
                            'Loaded plugin "{other}" conflicts with plugin '
                            '"{plugin_name}". Unable to load.'.format(
                                other=other,
                                plugin_name=plugin_name,
                            )
                        )
                        conflict = True
                if conflict:
                    continue

            # Check for requirements
            if hasattr(plugin_info, 'requires'):
                for other in plugin_info.requires:
                    if other not in self.manager and other not in self['load']:
                        warn(
                            'Plugin "{other}" is required by "{plugin_name}". '
                            'Please load "{other}" to avoid issues.'.format(
                                other=other,
                                plugin_name=plugin_name,
                            )
                        )

            # Load the plugin and get its instance
            plugin = self.manager[plugin_name]

            # Was the plugin unable to be loaded?
            if plugin is None:

                # Send a message that the plugin was not loaded
                self.logger.log_message(
                    self.prefix + self.translations[
                        'Unable to Load'
                    ].get_string(plugin=plugin_name)
                )

                # No need to go further
                return

            # Send a message that the plugin was loaded
            self.logger.log_message(
                self.prefix + self.translations[
                    'Successful Load'
                ].get_string(plugin=plugin_name)
            )

            # Fire the gg_plugin_load event
            with GG_Plugin_Loaded() as event:
                event.plugin = plugin_name
                event.plugin_type = plugin_type

# Get the _PluginQueue instance
plugin_queue = _PluginQueue()
