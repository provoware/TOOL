import datetime
import os
import sqlite3

from log import log_info


def add_template(
    db: str,
    name: str,
    title_tpl: str,
    text_tpl: str,
    genre: str | None = None,
):
    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO templates(name,title_tpl,text_tpl,genre) VALUES (?,?,?,?)",
            (name, title_tpl, text_tpl, genre),
        )
    log_info(f"Template gespeichert {name}")
    return True


def list_templates(db: str):
    with sqlite3.connect(db) as conn:
        return conn.execute(
            "SELECT id,name,title_tpl,text_tpl,genre FROM templates ORDER BY name"
        ).fetchall()


def delete_template(db: str, tid: int):
    with sqlite3.connect(db) as conn:
        conn.execute("DELETE FROM templates WHERE id=?", (tid,))
    log_info(f"Template gelöscht {tid}")
    return True


def update_template(
    db: str,
    tid: int,
    name: str,
    title_tpl: str,
    text_tpl: str,
    genre: str | None = None,
):
    with sqlite3.connect(db) as conn:
        conn.execute(
            "UPDATE templates SET name=?,title_tpl=?,text_tpl=?,genre=? WHERE id=?",
            (name, title_tpl, text_tpl, genre, tid),
        )
    log_info(f"Template geändert {tid}")
    return True


def render_template(row, seqnum: int, user_title: str = ""):
    _tid, name, title_tpl, text_tpl, genre = row
    today = datetime.date.today().isoformat()
    ctx = {
        "TITLE": user_title or name,
        "GENRE": genre or "",
        "DATE": today,
        "NUM": f"{seqnum:03}",
    }
    return title_tpl.format(**ctx), text_tpl.format(**ctx), genre
