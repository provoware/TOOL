"""Minimal interface for loading plugins."""

from plugin_manager import scan_and_load


def load_plugins(gui=None):
    """Scan the plugin directory and load plugins."""
    scan_and_load(gui)


if __name__ == "__main__":
    load_plugins()
