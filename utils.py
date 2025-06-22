
import sqlite3
import os
from shutil import copy2
from datetime import datetime

from log import log_info

DB = 'db/songarchiv.sqlite3'
os.makedirs('db', exist_ok=True)


def init_song_db(db):
    """Create the songs table if it does not exist."""
    with sqlite3.connect(db) as c:
        c.execute(
            'CREATE TABLE IF NOT EXISTS songs('
            'id INTEGER PRIMARY KEY,title TEXT,text TEXT,genre_id INTEGER,fav INTEGER DEFAULT 0,rating INTEGER DEFAULT 0)'
        )


def init_db(db):
    """Initialize application database with required tables."""
    init_song_db(db)
    with sqlite3.connect(db) as c:
        c.execute(
            'CREATE TABLE IF NOT EXISTS templates('
            'id INTEGER PRIMARY KEY,name TEXT,title_tpl TEXT,text_tpl TEXT,genre TEXT)'
        )
    log_info('Database initialized')


def get_theme(name, theme_dir):
    path = os.path.join(theme_dir, f'{name}.json')
    if os.path.isfile(path):
        return open(path, encoding='utf-8').read()
    return None


def list_themes(theme_dir):
    return [f[:-5] for f in os.listdir(theme_dir) if f.endswith('.json')]


def get_all_songs(db):
    init_song_db(db)
    with sqlite3.connect(db) as c:
        return c.execute('SELECT id,title,text,genre_id,fav,rating FROM songs').fetchall()


def search_songs(db, query='', genre_id=None):
    """Return songs matching a query and optional genre."""
    init_song_db(db)
    q = f"%{query}%"
    with sqlite3.connect(db) as c:
        if genre_id is not None:
            sql = 'SELECT id,title,text,genre_id,fav,rating FROM songs WHERE title LIKE ? AND genre_id=?'
            return c.execute(sql, (q, genre_id)).fetchall()
        sql = 'SELECT id,title,text,genre_id,fav,rating FROM songs WHERE title LIKE ?'
        return c.execute(sql, (q,)).fetchall()


def mark_favorite(db, song_id, fav=True):
    init_song_db(db)
    with sqlite3.connect(db) as c:
        c.execute('UPDATE songs SET fav=? WHERE id=?', (1 if fav else 0, song_id))


def rate_song(db, song_id, rating):
    init_song_db(db)
    rating = max(0, min(5, int(rating)))
    with sqlite3.connect(db) as c:
        c.execute('UPDATE songs SET rating=? WHERE id=?', (rating, song_id))


def init_playlist_db(db):
    """Create the playlist table if required."""
    with sqlite3.connect(db) as c:
        c.execute(
            'CREATE TABLE IF NOT EXISTS playlist('
            'id INTEGER PRIMARY KEY,title TEXT,file TEXT,pos INTEGER)'
        )


def get_playlist(db):
    init_playlist_db(db)
    with sqlite3.connect(db) as c:
        rows = c.execute('SELECT id,title,file,pos FROM playlist ORDER BY pos').fetchall()
    return [{'id': r[0], 'title': r[1], 'file': r[2], 'pos': r[3]} for r in rows]


def add_to_playlist(db, file_path):
    init_playlist_db(db)
    title = os.path.splitext(os.path.basename(file_path))[0]
    with sqlite3.connect(db) as c:
        cur = c.execute('SELECT MAX(pos) FROM playlist')
        maxpos = cur.fetchone()[0] or 0
        c.execute('INSERT INTO playlist(title,file,pos) VALUES (?,?,?)', (title, file_path, maxpos + 1))


def remove_from_playlist(db, pid):
    init_playlist_db(db)
    with sqlite3.connect(db) as c:
        cur = c.execute('SELECT pos FROM playlist WHERE id=?', (pid,))
        row = cur.fetchone()
        if not row:
            return
        pos = row[0]
        c.execute('DELETE FROM playlist WHERE id=?', (pid,))
        c.execute('UPDATE playlist SET pos=pos-1 WHERE pos>?', (pos,))


def export_playlist_m3u(db, out_file):
    """Export playlist to an M3U file."""
    pl = get_playlist(db)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for item in pl:
            f.write(f"{item['file']}\n")


def export_playlist_csv(db, out_file):
    """Export playlist to a CSV file."""
    import csv

    pl = get_playlist(db)
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'title', 'file'])
        for it in pl:
            w.writerow([it['id'], it['title'], it['file']])


def move_playlist_item(db, from_idx, to_idx):
    """Move an item in the playlist."""
    if from_idx == to_idx:
        return
    pl = get_playlist(db)
    if from_idx < 0 or to_idx < 0 or from_idx >= len(pl) or to_idx >= len(pl):
        return
    item = pl.pop(from_idx)
    pl.insert(to_idx, item)
    with sqlite3.connect(db) as c:
        for pos, row in enumerate(pl):
            c.execute('UPDATE playlist SET pos=? WHERE id=?', (pos, row['id']))


def backup_database(src, backup_dir):
    """Create a timestamped copy of the database."""
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(backup_dir, f'{os.path.basename(src)}.{ts}.bak')
    copy2(src, dest)
    log_info(f'Backup {dest}')
    return dest


def restore_database(src, backup_file):
    """Restore the database from a backup file."""
    copy2(backup_file, src)
    log_info(f'Restored database from {backup_file}')


def read_metadata(file_path):
    """Return basic metadata for an audio file if possible."""
    info = {'title': os.path.splitext(os.path.basename(file_path))[0]}
    try:
        import mutagen
        audio = mutagen.File(file_path)
        if audio:
            title = audio.tags.get('TIT2') if hasattr(audio, 'tags') else None
            if title:
                info['title'] = str(title)
    except Exception as e:
        log_info(f'Metadata read failed: {e}')
    return info
