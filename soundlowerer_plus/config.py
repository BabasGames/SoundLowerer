import os, json, shutil, logging

APP_NAME = "SoundLowerer"
CONFIG_FILE = "volume_control_services.json"

def _get_real_home():
    """Retourne le home de l'utilisateur réel, même sous sudo."""
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user and os.getuid() == 0:
        import pwd
        try:
            return pwd.getpwnam(sudo_user).pw_dir
        except KeyError:
            pass
    return os.path.expanduser("~")

def config_dir():
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        return os.path.join(base, APP_NAME)
    else:
        home = _get_real_home()
        return os.path.join(home, ".config", APP_NAME)

def ensure_config_dir():
    d = config_dir()
    os.makedirs(d, exist_ok=True)
    return d

def config_path():
    return os.path.join(ensure_config_dir(), CONFIG_FILE)

def migrate_if_needed(legacy_path="./volume_control_services.json"):
    newp = config_path()
    if not os.path.exists(newp) and os.path.exists(legacy_path):
        try:
            shutil.copyfile(legacy_path, newp)
        except Exception:
            pass

DEFAULT_SETTINGS = {
    "resume_on_start": True,
    "active_services": []
}

def load_config():
    migrate_if_needed()
    p = config_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                # S'assurer que les paramètres par défaut existent
                if "settings" not in data:
                    data["settings"] = {}
                for key, default in DEFAULT_SETTINGS.items():
                    if key not in data["settings"]:
                        data["settings"][key] = default
                return data
        except Exception:
            return {"services": [], "settings": dict(DEFAULT_SETTINGS)}
    return {"services": [], "settings": dict(DEFAULT_SETTINGS)}

def save_config(data: dict):
    p = config_path()
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def setup_logging():
    """Configure le logging de l'application"""
    log_file = os.path.join(ensure_config_dir(), "soundlowerer.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Aussi dans la console
        ]
    )
    return logging.getLogger('SoundLowerer')

# Logger global
logger = None

def get_logger():
    global logger
    if logger is None:
        logger = setup_logging()
    return logger
