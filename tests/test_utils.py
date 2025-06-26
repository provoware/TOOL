import os
import json
import tempfile
from utils import (
    init_playlist_db,
    get_playlist,
    add_to_playlist,
    remove_from_playlist,
    init_song_db,
    get_theme,
    list_themes,
)

def test_playlist_cycle():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, 'pl.sqlite3')
        assert init_playlist_db(db)
        assert get_playlist(db) == []
        f = os.path.join(tmp, 'song.mp3')
        open(f, 'w').close()
        assert add_to_playlist(db, f)
        items = get_playlist(db)
        assert len(items) == 1
        assert items[0]['file'] == f
        assert remove_from_playlist(db, items[0]['id'])
        assert get_playlist(db) == []

def test_song_db_init():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, 'songs.sqlite3')
        assert init_song_db(db)


def test_theme_utils():
    with tempfile.TemporaryDirectory() as tmp:
        data = {'color': 'x'}
        with open(os.path.join(tmp, 'dark.json'), 'w') as f:
            json.dump(data, f)
        with open(os.path.join(tmp, 'light.json'), 'w') as f:
            json.dump({'color': 'y'}, f)
        names = list_themes(tmp)
        assert set(names) == {'dark', 'light'}
        assert get_theme('dark', tmp) == data
