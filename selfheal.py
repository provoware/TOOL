"""Simple self-healing helpers for SongArchiv."""

import os
from utils import init_song_db, init_playlist_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONG_DB = os.path.join(BASE_DIR, "db", "songarchiv.sqlite3")
PLAYLIST_DB = os.path.join(BASE_DIR, "db", "songarchiv_playlist.sqlite3")


def repair():
    """Ensure databases exist and have correct schema."""

    init_song_db(SONG_DB)
    init_playlist_db(PLAYLIST_DB)
    print("Databases verified")


if __name__ == "__main__":
    repair()
