import importlib.util, os, json, shutil, zipfile, hashlib
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


def install_plugin(zip_file):
    """Install a plugin from a ZIP archive."""
    try:
        with zipfile.ZipFile(zip_file) as z:
            name = os.path.splitext(os.path.basename(zip_file))[0]
            dest = os.path.join(PLUGIN_DIR, name)
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            z.extractall(dest)
        log_info(f'Plugin installed {name}')
        return True
    except Exception as e:
        log_error('Plugin-Install', e)
        return False


def checksum(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()
