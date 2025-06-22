"""Simple plugin loader used by the application."""

from typing import Optional

import plugin_manager


def load_plugins(gui: Optional[object] = None) -> None:
    """Scan the ``plugins`` directory and load all available plugins."""

    plugin_manager.scan_and_load(gui)

