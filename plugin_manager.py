"""Compatibility wrapper for the plugin management functions."""
from plugin import PLUGIN_DIR, load_plugins, install_plugin

# maintain old API name
scan_and_load = load_plugins
