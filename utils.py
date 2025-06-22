
import sqlite3
import os
from typing import List, Dict

from log import log_info

DB = "db/songarchiv.sqlite3"
os.makedirs("db", exist_ok=True)


def _ensure_song_table(db: str) -> None:
    """Create the songs table if it does not yet exist."""
    with sqlite3.connect(db) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS songs("
            "id INTEGER PRIMARY KEY,"
            "title TEXT,"
            "text TEXT,"
            "genre_id INTEGER)"
        )


def _ensure_playlist_table(db: str) -> None:
    """Create the playlist table if required."""
    with sqlite3.connect(db) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS playlist("
            "id INTEGER PRIMARY KEY,"
            "file TEXT,"
            "title TEXT)"
        )


def init_song_db(db: str) -> None:
    """Initialise the song database."""
    _ensure_song_table(db)
    log_info(f"Song-DB initialisiert {db}")


def init_playlist_db(db: str) -> None:
    """Initialise the playlist database."""
    _ensure_playlist_table(db)
    log_info(f"Playlist-DB initialisiert {db}")


def init_db(db: str) -> None:
    """Initialise all required database tables."""
    init_song_db(db)
    init_playlist_db(db)


def get_all_songs(db: str) -> List[tuple]:
    """Return all songs from the given database."""
    _ensure_song_table(db)
    with sqlite3.connect(db) as c:
        return c.execute(
            "SELECT id, title, text, genre_id FROM songs"
        ).fetchall()


def get_playlist(db: str) -> List[Dict[str, str]]:
    """Return playlist entries as a list of dictionaries."""
    _ensure_playlist_table(db)
    with sqlite3.connect(db) as c:
        rows = c.execute(
            "SELECT id, file, title FROM playlist ORDER BY id"
        ).fetchall()
    return [
        {"id": r[0], "file": r[1], "title": r[2]} for r in rows
    ]


def add_to_playlist(db: str, file_path: str) -> None:
    """Add a file to the playlist."""
    _ensure_playlist_table(db)
    title = os.path.basename(file_path)
    with sqlite3.connect(db) as c:
        c.execute(
            "INSERT INTO playlist(file, title) VALUES (?, ?)",
            (file_path, title),
        )
    log_info(f"Zur Playlist hinzugefügt {title}")


def remove_from_playlist(db: str, entry_id: int) -> None:
    """Remove an entry from the playlist by id."""
    _ensure_playlist_table(db)
    with sqlite3.connect(db) as c:
        c.execute("DELETE FROM playlist WHERE id=?", (entry_id,))
    log_info(f"Playlist-Eintrag entfernt {entry_id}")


def get_theme(name: str, theme_dir: str) -> str:
    """Return the GUI theme name from files in *theme_dir*.

    If no theme file is found a default theme name is returned."""
    os.makedirs(theme_dir, exist_ok=True)
    path = os.path.join(theme_dir, f"{name}.txt")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "DarkBlack1"


def list_themes(theme_dir: str) -> List[str]:
    """List available themes in *theme_dir*."""
    os.makedirs(theme_dir, exist_ok=True)
    names = []
    for f in os.listdir(theme_dir):
        if f.endswith(".txt"):
            names.append(os.path.splitext(f)[0])
    return names

