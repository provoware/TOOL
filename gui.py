
import os
import sys
import PySimpleGUI as sg
import pyttsx3
from audio import AudioPlayer
from utils import (
    init_playlist_db,
    get_playlist,
    add_to_playlist,
    remove_from_playlist,
    init_song_db,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST_DB = os.path.join(BASE_DIR,'db','songarchiv_playlist.sqlite3')
SONG_DB = os.path.join(BASE_DIR,'db','songarchiv.sqlite3')

init_playlist_db(PLAYLIST_DB)
init_song_db(SONG_DB)

player = AudioPlayer()
_engine = None

def speak(text: str) -> None:
    """Speak text using pyttsx3 if available."""
    global _engine
    if _engine is None:
        try:
            _engine = pyttsx3.init()
        except Exception:
            _engine = False
    if _engine:
        try:
            _engine.say(text)
            _engine.runAndWait()
        except Exception:
            pass

def refresh_playlist(window):
    pl = get_playlist(PLAYLIST_DB)
    window['-LIST-'].update([item['title'] for item in pl])
    return pl


def start_gui():
    """Start the accessible GUI."""
    sg.theme('DarkBlack1')
    sg.set_options(font=('DejaVu Sans', 14))

    layout = [
        [sg.Text('Playlist', font=('DejaVu Sans', 16, 'bold'))],
        [sg.Listbox(values=[], size=(40, 10), key='-LIST-', enable_events=True)],
        [
            sg.Button('Abspielen', key='-PLAY-', tooltip='Abspielen (Enter)', bind_return_key=True),
            sg.Button('Pause', key='-PAUSE-', tooltip='Pause/Weiter (P)'),
            sg.Button('Stopp', key='-STOP-', tooltip='Wiedergabe stoppen (S)'),
        ],
        [sg.Button('Hinzufügen', tooltip='Dateien hinzufügen (A)'), sg.Button('Entfernen', tooltip='Ausgewählte entfernen (D)')],
        [sg.Text('Lautstärke'), sg.Slider((0, 1), default_value=0.8, resolution=0.05, orientation='h', key='-VOL-', enable_events=True)],
        [sg.StatusBar('Gestoppt', key='-STATUS-')],
    ]

    window = sg.Window('Audio Player', layout, finalize=True)
    playlist = refresh_playlist(window)
    current_idx = 0

    speak('Bereit')

    while True:
        ev, vals = window.read(timeout=100)
        if ev in (sg.WINDOW_CLOSED, 'Exit'):
            break
        if ev == '-LIST-':
            sel = vals['-LIST-']
            if sel:
                current_idx = window['-LIST-'].get_indexes()[0]
                speak(sel[0])
        if ev == 'Hinzufügen':
            files = sg.popup_get_file('Datei auswählen', multiple_files=True, file_types=(('Audio', '*.mp3;*.wav;*.ogg'),))
            if files:
                for f in files.split(';'):
                    add_to_playlist(PLAYLIST_DB, f)
                playlist = refresh_playlist(window)
                speak('Datei hinzugefügt')
        if ev == 'Entfernen':
            if playlist:
                remove_from_playlist(PLAYLIST_DB, playlist[current_idx]['id'])
                playlist = refresh_playlist(window)
                current_idx = 0
                speak('Eintrag entfernt')
        if ev == '-PLAY-':
            if playlist:
                res = player.play(playlist[current_idx]['file'])
                if res is not True:
                    sg.popup_error(res)
                else:
                    speak('Abspielen')
        if ev == '-PAUSE-':
            player.toggle_pause()
            speak('Pause')
        if ev == '-STOP-':
            player.stop()
            speak('Stopp')
        if ev == '-VOL-':
            player.set_volume(vals['-VOL-'])
            speak(f'Lautstärke {int(vals["-VOL-"]*100)} Prozent')
        window['-STATUS-'].update(player.status())

    window.close()
