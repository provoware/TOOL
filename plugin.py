"""Plugin management utilities for SongArchiv.

This module discovers and loads plugins from the :data:`plugins` directory. A
plugin is a folder containing a ``manifest.json`` file with at least an
``entrypoint`` key pointing to the python file that should be executed.  When a
module defines ``register_menu(gui)`` it will be called with the GUI instance
once loaded.

Optionally ``install_plugin`` allows installing or updating a plugin from a
zip archive.
"""

import importlib.util
import json
import os
import shutil
import zipfile
from typing import Iterator, Tuple, Dict, Any

from log import log_info, log_error

PLUGIN_DIR = "plugins"
os.makedirs(PLUGIN_DIR, exist_ok=True)


def discover_plugins() -> Iterator[Tuple[str, Dict[str, Any]]]:
    """Yield plugin directories and loaded manifest information."""
    for folder in os.listdir(PLUGIN_DIR):
        path = os.path.join(PLUGIN_DIR, folder)
        manifest = os.path.join(path, "manifest.json")
        if os.path.isfile(manifest):
            try:
                yield path, json.load(open(manifest, encoding="utf-8"))
            except Exception as exc:
                log_error("Manifest", exc)


def load_plugins(gui=None) -> None:
    """Load all discovered plugins.

    If a loaded module exposes ``register_menu`` and ``gui`` is provided,
    ``register_menu`` is called to allow the plugin to extend the GUI.
    """
    for path, info in discover_plugins():
        try:
            name = info.get("name", os.path.basename(path))
            spec = importlib.util.spec_from_file_location(
                name, os.path.join(path, info["entrypoint"])
            )
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)  # type: ignore
                if hasattr(mod, "register_menu") and gui:
                    mod.register_menu(gui)
                log_info(f"Plugin loaded {name}")
        except Exception as exc:
            log_error("Plugin-Load", exc)


def install_plugin(archive: str) -> str:
    """Install or update a plugin from a zip archive.

    The archive should contain a single root folder holding ``manifest.json``.
    Existing plugins with the same folder name will be replaced.
    Returns the name of the installed plugin folder.
    """
    with zipfile.ZipFile(archive, "r") as zf:
        root = zf.namelist()[0].split("/")[0]
        temp_dir = os.path.join(PLUGIN_DIR, f".{root}_tmp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        zf.extractall(temp_dir)
        if not os.path.isfile(os.path.join(temp_dir, "manifest.json")):
            shutil.rmtree(temp_dir)
            raise ValueError("Archive missing manifest.json")
        dest = os.path.join(PLUGIN_DIR, root)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        os.rename(temp_dir, dest)
    log_info(f"Plugin installed {root}")
    return root

