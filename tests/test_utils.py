import os
import sqlite3
import tempfile

import utils


def test_playlist_crud():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    try:
        utils.init_playlist_db(db_path)
        utils.add_to_playlist(db_path, '/tmp/song1.mp3')
        utils.add_to_playlist(db_path, '/tmp/song2.mp3')
        pl = utils.get_playlist(db_path)
        assert len(pl) == 2
        ids = [entry['id'] for entry in pl]
        utils.remove_from_playlist(db_path, ids[0])
        pl = utils.get_playlist(db_path)
        assert len(pl) == 1
    finally:
        os.remove(db_path)


def test_init_db_creates_tables():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    try:
        utils.init_db(db_path)
        with sqlite3.connect(db_path) as c:
            tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        assert 'songs' in tables
        assert 'playlist' in tables
    finally:
        os.remove(db_path)
