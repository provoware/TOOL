
import sqlite3
import os
from log import log_info

# Default path used when the helper functions are called without explicit path
DB = os.path.join('db', 'songarchiv.sqlite3')
os.makedirs('db', exist_ok=True)


def init_song_db(path: str) -> None:
    """Create the songs table if it does not yet exist."""
    with sqlite3.connect(path) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS songs("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "title TEXT,"
            "text TEXT,"
            "genre_id INTEGER)"
        )
    log_info(f'Init songs DB {path}')


def init_playlist_db(path: str) -> None:
    """Create the playlist table."""
    with sqlite3.connect(path) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS playlist("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "file TEXT NOT NULL,"
            "title TEXT NOT NULL)"
        )
    log_info(f'Init playlist DB {path}')


def init_db(path: str) -> None:
    """Initialise both song and playlist databases."""
    init_song_db(path)
    init_playlist_db(os.path.join(os.path.dirname(path), 'songarchiv_playlist.sqlite3'))


def get_all_songs(path: str):
    """Return all songs from the database."""
    init_song_db(path)
    with sqlite3.connect(path) as con:
        return con.execute(
            'SELECT id, title, text, genre_id FROM songs'
        ).fetchall()


def get_playlist(path: str):
    """Return playlist items as list of dictionaries."""
    init_playlist_db(path)
    with sqlite3.connect(path) as con:
        rows = con.execute('SELECT id, file, title FROM playlist ORDER BY id').fetchall()
    return [{'id': r[0], 'file': r[1], 'title': r[2]} for r in rows]


def add_to_playlist(path: str, file_path: str) -> None:
    """Add a file to the playlist."""
    title = os.path.basename(file_path)
    with sqlite3.connect(path) as con:
        con.execute('INSERT INTO playlist(file, title) VALUES (?, ?)', (file_path, title))
    log_info(f'Added to playlist: {file_path}')


def remove_from_playlist(path: str, item_id: int) -> None:
    """Remove an entry from the playlist."""
    with sqlite3.connect(path) as con:
        con.execute('DELETE FROM playlist WHERE id=?', (item_id,))
    log_info(f'Removed from playlist: {item_id}')


def get_theme(name: str, theme_dir: str):
    """Load a theme file by name or return the name if none found."""
    path = os.path.join(theme_dir, f'{name}.json')
    if os.path.isfile(path):
        import json

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return name  # fallback to PySimpleGUI builtin theme name


def list_themes(theme_dir: str):
    """List available theme names."""
    if not os.path.isdir(theme_dir):
        return []
    names = []
    for f in os.listdir(theme_dir):
        if f.endswith('.json'):
            names.append(os.path.splitext(f)[0])
    return names

