
import sqlite3
import os
import json

from log import log_info

DB = "db/songarchiv.sqlite3"
os.makedirs("db", exist_ok=True)


def init_db(db_path: str) -> None:
    """Create the main songs table if it doesn't exist."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                title TEXT,
                text TEXT,
                genre_id INTEGER
            )
            """
        )
    log_info(f"DB initialisiert {db_path}")


def init_song_db(db_path: str) -> None:
    init_db(db_path)


def init_playlist_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist (
                id INTEGER PRIMARY KEY,
                file TEXT NOT NULL,
                title TEXT
            )
            """
        )
    log_info(f"Playlist-DB initialisiert {db_path}")


def add_to_playlist(db_path: str, file_path: str) -> None:
    title = os.path.basename(file_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO playlist(file, title) VALUES (?, ?)",
            (file_path, title),
        )
    log_info(f"Zur Playlist hinzugefügt: {title}")


def remove_from_playlist(db_path: str, entry_id: int) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM playlist WHERE id=?", (entry_id,))
    log_info(f"Playlist-Eintrag gelöscht {entry_id}")


def get_playlist(db_path: str):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute("SELECT id, file, title FROM playlist ORDER BY id").fetchall()
        return [dict(r) for r in res]


def list_themes(theme_dir: str):
    if not os.path.isdir(theme_dir):
        return []
    return [f[:-5] for f in os.listdir(theme_dir) if f.endswith(".json")]


def get_theme(name: str, theme_dir: str):
    path = os.path.join(theme_dir, f"{name}.json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def get_all_songs(db: str):
    with sqlite3.connect(db) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY,title TEXT,text TEXT,genre_id INTEGER)"
        )
        return c.execute("SELECT id,title,text,genre_id FROM songs").fetchall()

