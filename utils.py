
import sqlite3
import os
import json

from log import log_info

DB = "db/songarchiv.sqlite3"
os.makedirs("db", exist_ok=True)


def get_all_songs(db):
    """Return all songs from the song database."""
    with sqlite3.connect(db) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY,title TEXT,text TEXT,genre_id INTEGER)"
        )
        return c.execute(
            "SELECT id,title,text,genre_id FROM songs"
        ).fetchall()


# ---- Playlist helpers -----------------------------------------------------


def init_playlist_db(path):
    """Create the playlist database with a simple schema."""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with sqlite3.connect(path) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS playlist(id INTEGER PRIMARY KEY AUTOINCREMENT,file TEXT,title TEXT)"
        )
    log_info(f"Playlist-DB init {path}")
    return True


def get_playlist(path):
    """Return the playlist as a list of dictionaries."""

    with sqlite3.connect(path) as c:
        rows = c.execute(
            "SELECT id,file,title FROM playlist ORDER BY id"
        ).fetchall()
        return [
            {"id": r[0], "file": r[1], "title": r[2]}
            for r in rows
        ]


def add_to_playlist(path, file_path):
    """Add an audio file to the playlist."""

    title = os.path.basename(file_path)
    with sqlite3.connect(path) as c:
        c.execute(
            "INSERT INTO playlist(file,title) VALUES (?,?)",
            (file_path, title),
        )
    log_info(f"Playlist add {file_path}")
    return True


def remove_from_playlist(path, item_id):
    """Remove an entry from the playlist."""

    with sqlite3.connect(path) as c:
        c.execute("DELETE FROM playlist WHERE id=?", (item_id,))
    log_info(f"Playlist remove {item_id}")
    return True


# ---- Song DB helpers ------------------------------------------------------


def init_song_db(path):
    """Ensure the songs table exists."""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with sqlite3.connect(path) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY,title TEXT,text TEXT,genre_id INTEGER)"
        )
    log_info(f"Song-DB init {path}")
    return True


def init_db(path):
    """Alias for initialising the main song database."""

    return init_song_db(path)


# ---- Theme helpers -------------------------------------------------------


def get_theme(name, theme_dir):
    """Load a theme JSON by name if it exists."""

    path = os.path.join(theme_dir, f"{name}.json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def list_themes(theme_dir):
    """Return a list of available theme names."""

    if not os.path.isdir(theme_dir):
        return []
    return [
        os.path.splitext(fn)[0]
        for fn in os.listdir(theme_dir)
        if fn.endswith(".json")
    ]

