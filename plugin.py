"""Simple plugin management utilities."""

import os
import shutil
import zipfile

from log import log_info, log_error
from plugin_manager import scan_and_load

PLUGIN_DIR = "plugins"
os.makedirs(PLUGIN_DIR, exist_ok=True)


def load_plugins(gui=None) -> None:
    """Load all plugins found in :data:`PLUGIN_DIR`."""
    scan_and_load(gui)


def install_plugin(zip_path: str) -> bool:
    """Install a plugin from a ZIP archive."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            name = os.path.splitext(os.path.basename(zip_path))[0]
            target = os.path.join(PLUGIN_DIR, name)
            os.makedirs(target, exist_ok=True)
            zf.extractall(target)
        log_info(f"Plugin installiert {name}")
        return True
    except Exception as e:
        log_error("Plugin-Install", e)
        return False


def remove_plugin(name: str) -> bool:
    """Remove an installed plugin."""
    path = os.path.join(PLUGIN_DIR, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
        log_info(f"Plugin entfernt {name}")
        return True
    return False

