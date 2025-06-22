import os
from gui import start_gui
from utils import init_db, get_theme, list_themes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "songarchiv.sqlite3")
THEME_DIR = os.path.join(BASE_DIR, "themes")
BACKUP_DIR = os.path.join(BASE_DIR, "db", "backup")

def first_start_setup():
    os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        print("Erstelle Datenbank...")
        init_db(DB_PATH)

def main():
    first_start_setup()
    theme_name = "dark"
    theme = get_theme(theme_name, THEME_DIR)
    themes = list_themes(THEME_DIR)
    start_gui(DB_PATH, theme, themes, THEME_DIR, BACKUP_DIR)

if __name__ == "__main__":
    main()
