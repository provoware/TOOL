
import sqlite3, os
from log import log_info
DB='db/songarchiv.sqlite3'; os.makedirs('db',exist_ok=True)
def get_all_songs(db): 
    with sqlite3.connect(db) as c: 
        c.execute('CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY,title TEXT,text TEXT,genre_id INTEGER)')
        return c.execute('SELECT id,title,text,genre_id FROM songs').fetchall()
