import json
import os
import sqlite3

from log import log_info


DB = "db/songarchiv.sqlite3"
os.makedirs("db", exist_ok=True)


# ---------------------------------------------------------------------------
# Song database
# ---------------------------------------------------------------------------

def init_db(db: str) -> None:
    """Create the main song database if it does not yet exist."""
    os.makedirs(os.path.dirname(db), exist_ok=True)
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS songs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                text TEXT,
                genre_id INTEGER
            )
            """
        )
    log_info(f"DB initialisiert {db}")


def init_song_db(db: str) -> None:
    init_db(db)


def get_all_songs(db: str):
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT id,title,text,genre_id FROM songs"
        ).fetchall()


# ---------------------------------------------------------------------------
# Playlist handling
# ---------------------------------------------------------------------------

def init_playlist_db(db: str) -> None:
    os.makedirs(os.path.dirname(db), exist_ok=True)
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file TEXT NOT NULL,
                title TEXT NOT NULL
            )
            """
        )
    log_info(f"Playlist-DB initialisiert {db}")


def add_to_playlist(db: str, file_path: str) -> None:
    title = os.path.basename(file_path)
    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO playlist(file,title) VALUES (?,?)",
            (file_path, title),
        )


def remove_from_playlist(db: str, pid: int) -> None:
    with sqlite3.connect(db) as conn:
        conn.execute("DELETE FROM playlist WHERE id=?", (pid,))


def get_playlist(db: str):
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id,file,title FROM playlist ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

def get_theme(name: str, theme_dir: str):
    path = os.path.join(theme_dir, f"{name}.json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def list_themes(theme_dir: str):
    if not os.path.isdir(theme_dir):
        return []
    return [f[:-5] for f in os.listdir(theme_dir) if f.endswith(".json")]
