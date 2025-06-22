import datetime
import sqlite3
from log import log_info
def add_template(db,name,title_tpl,text_tpl,genre=None):
    with sqlite3.connect(db) as c:
        c.execute("INSERT INTO templates(name,title_tpl,text_tpl,genre) VALUES (?,?,?,?)",(name,title_tpl,text_tpl,genre))
    log_info(f"Template gespeichert {name}"); return True
def list_templates(db):
    with sqlite3.connect(db) as c:
        return c.execute("SELECT id,name,title_tpl,text_tpl,genre FROM templates ORDER BY name").fetchall()
def delete_template(db,id):
    with sqlite3.connect(db) as c: c.execute("DELETE FROM templates WHERE id=?", (id,))
    log_info(f'Template gelöscht {id}'); return True
def update_template(db,id,name,title_tpl,text_tpl,genre=None):
    with sqlite3.connect(db) as c:
        c.execute("UPDATE templates SET name=?,title_tpl=?,text_tpl=?,genre=? WHERE id=?",(name,title_tpl,text_tpl,genre,id))
    log_info(f"Template geändert {id}"); return True
def render_template(row,seqnum,user_title=''):
    _id,name,title_tpl,text_tpl,genre=row
    today=datetime.date.today().isoformat()
    ctx={"TITLE":user_title or name,"GENRE":genre or "","DATE":today,"NUM":f'{seqnum:03}'}
    return title_tpl.format(**ctx), text_tpl.format(**ctx), genre
