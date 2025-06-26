import os
import PySimpleGUI as sg

from audio import AudioPlayer
from utils import (
    init_playlist_db,
    get_playlist,
    add_to_playlist,
    remove_from_playlist,
    init_song_db,
)


def start_gui(db_path, theme=None, themes=None, theme_dir=None, backup_dir=None):
    """Start the simple audio player GUI."""

    base_dir = os.path.dirname(os.path.abspath(__file__))
    playlist_db = os.path.join(base_dir, "db", "songarchiv_playlist.sqlite3")

    init_playlist_db(playlist_db)
    init_song_db(db_path)

    player = AudioPlayer()

    def refresh_playlist(win):
        pl = get_playlist(playlist_db)
        win["-LIST-"].update([item["title"] for item in pl])
        return pl

    sg.theme(theme or "DefaultNoMoreNag")

    layout = [
        [sg.Text("Playlist", font=("DejaVu Sans", 16, "bold"))],
        [sg.Listbox(values=[], size=(40, 10), key="-LIST-", enable_events=True)],
        [
            sg.Button("Abspielen", key="-PLAY-"),
            sg.Button("Pause", key="-PAUSE-"),
            sg.Button("Stopp", key="-STOP-"),
        ],
        [sg.Button("Hinzufügen"), sg.Button("Entfernen")],
        [
            sg.Text("Lautstärke"),
            sg.Slider(
                (0, 1),
                default_value=0.8,
                resolution=0.05,
                orientation="h",
                key="-VOL-",
                enable_events=True,
            ),
        ],
        [sg.StatusBar("Gestoppt", key="-STATUS-")],
    ]

    window = sg.Window("Audio Player", layout, finalize=True)
    playlist = refresh_playlist(window)
    current_idx = 0

    while True:
        ev, vals = window.read(timeout=100)
        if ev in (sg.WINDOW_CLOSED, "Exit"):
            break
        if ev == "-LIST-":
            sel = vals["-LIST-"]
            if sel:
                current_idx = window["-LIST-"].get_indexes()[0]
        if ev == "Hinzufügen":
            files = sg.popup_get_file(
                "Datei auswählen",
                multiple_files=True,
                file_types=(("Audio", "*.mp3;*.wav;*.ogg"),),
            )
            if files:
                for f in files.split(";"):
                    add_to_playlist(playlist_db, f)
                playlist = refresh_playlist(window)
        if ev == "Entfernen":
            if playlist:
                remove_from_playlist(playlist_db, playlist[current_idx]["id"])
                playlist = refresh_playlist(window)
                current_idx = 0
        if ev == "-PLAY-":
            if playlist:
                res = player.play(playlist[current_idx]["file"])
                if res is not True:
                    sg.popup_error(res)
        if ev == "-PAUSE-":
            player.toggle_pause()
        if ev == "-STOP-":
            player.stop()
        if ev == "-VOL-":
            player.set_volume(vals["-VOL-"])
        window["-STATUS-"].update(player.status())

    window.close()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SONG_DB = os.path.join(BASE_DIR, "db", "songarchiv.sqlite3")
    start_gui(SONG_DB)
