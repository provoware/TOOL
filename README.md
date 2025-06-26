# SongArchiv

Ein minimaler Audio‑Player mit Playlist‑Unterstützung.

## Installation

```bash
pip install -r requirements.txt
```

## Anwendung

Die grafische Oberfläche wird über `main.py` gestartet:

```bash
python main.py
```

Die Datenbanken werden dabei automatisch im Ordner `db` angelegt.

## Abhängigkeiten

Siehe `requirements.txt` für alle benötigten Pakete. Wichtig ist vor allem `pygame` für die Wiedergabe und `PySimpleGUI` für die Benutzeroberfläche.

## Tests

Automatische Tests liegen im Verzeichnis `tests`. Sie können mit `pytest` oder über das Skript `selftest.py` gestartet werden:

```bash
python selftest.py
```

Falls ein Test fehlschlägt, versucht `selftest.py` automatisch, die Datenbanken zu reparieren und startet die Tests erneut.

Weitere Hinweise zur Einrichtung finden Sie in der Datei `ANLEITUNG.md`.
