# ../gungame/core/events/resource.py

"""GunGame event resource file functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package
from path import Path

# Source.Python
from events.resource import ResourceFile

# GunGame
from .storage import gg_resource_list


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GGResourceFile',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GGResourceFile(ResourceFile):
    """Class used for GunGame res files."""

    def __init__(self, file_path, *events):
        """Add 'gungame' to the path before initialization."""
        super().__init__(Path('gungame') / file_path, *events)
        gg_resource_list.append(self)
