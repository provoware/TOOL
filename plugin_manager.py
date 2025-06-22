import importlib.util
import json
import os
from log import log_info, log_error
PLUGIN_DIR='plugins'; os.makedirs(PLUGIN_DIR,exist_ok=True)
def scan_and_load(gui=None):
    for folder in os.listdir(PLUGIN_DIR):
        path=os.path.join(PLUGIN_DIR,folder)
        mf=os.path.join(path,'manifest.json')
        if not os.path.isfile(mf): continue
        try:
            info=json.load(open(mf,encoding='utf-8'))
            spec=importlib.util.spec_from_file_location(folder, os.path.join(path,info['entrypoint']))
            mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            if hasattr(mod,'register_menu') and gui: mod.register_menu(gui)
            log_info(f"Plugin geladen {folder}")
        except Exception as e: log_error("Plugin-Load",e)
