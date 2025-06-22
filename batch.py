import csv
import os
import sqlite3
import zipfile

from log import log_info


def batch_rename(db: str, ids: list[int], prefix: str = "", suffix: str = ""):
    with sqlite3.connect(db) as conn:
        for i in ids:
            title = conn.execute(
                "SELECT title FROM songs WHERE id=?", (i,)
            ).fetchone()[0]
            conn.execute(
                "UPDATE songs SET title=? WHERE id=?",
                (f"{prefix}{title}{suffix}", i),
            )
    log_info(f"Batch-Rename {len(ids)}")
    return True


def batch_genre_change(db: str, ids: list[int], new_gid: int):
    with sqlite3.connect(db) as conn:
        for i in ids:
            conn.execute(
                "UPDATE songs SET genre_id=? WHERE id=?", (new_gid, i)
            )
    log_info(f"Batch-Genre {len(ids)}")
    return True


def batch_export(db: str, ids: list[int], out: str):
    from utils import get_all_songs

    songs = [s for s in get_all_songs(db) if s[0] in ids]
    csvf = "songs.csv"
    with open(csvf, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Title", "Text", "Genre"])
        w.writerows([[s[0], s[1], s[2], s[3]] for s in songs])
    with zipfile.ZipFile(out, "w") as z:
        z.write(csvf)
    os.remove(csvf)
    log_info(f"Batch-Export {out}")
    return True
