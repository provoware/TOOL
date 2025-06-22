import importlib.util
import json
import os

from log import log_error, log_info

PLUGIN_DIR = "plugins"
os.makedirs(PLUGIN_DIR, exist_ok=True)


def scan_and_load(gui=None) -> None:
    """Load all plugins found in ``PLUGIN_DIR``."""
    for folder in os.listdir(PLUGIN_DIR):
        path = os.path.join(PLUGIN_DIR, folder)
        manifest = os.path.join(path, "manifest.json")
        if not os.path.isfile(manifest):
            continue
        try:
            with open(manifest, encoding="utf-8") as f:
                info = json.load(f)
            spec = importlib.util.spec_from_file_location(
                folder, os.path.join(path, info["entrypoint"])
            )
            module = importlib.util.module_from_spec(spec)
            assert spec.loader  # for type checkers
            spec.loader.exec_module(module)
            if hasattr(module, "register_menu") and gui:
                module.register_menu(gui)
            log_info(f"Plugin geladen {folder}")
        except Exception as exc:  # pragma: no cover - plugin dependent
            log_error("Plugin-Load", exc)
