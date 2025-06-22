
import PySimpleGUI as sg, os, sys
from audio import AudioPlayer
from utils import init_playlist_db, get_playlist, add_to_playlist, remove_from_playlist,     init_song_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYLIST_DB = os.path.join(BASE_DIR,'db','songarchiv_playlist.sqlite3')
SONG_DB = os.path.join(BASE_DIR,'db','songarchiv.sqlite3')

init_playlist_db(PLAYLIST_DB)
init_song_db(SONG_DB)

player = AudioPlayer()

def refresh_playlist(window):
    pl = get_playlist(PLAYLIST_DB)
    window['-LIST-'].update([item['title'] for item in pl])
    return pl

sg.theme('DefaultNoMoreNag')
layout = [
    [sg.Text('Playlist', font=('DejaVu Sans',16,'bold'))],
    [sg.Listbox(values=[], size=(40,10), key='-LIST-', enable_events=True)],
    [sg.Button('Abspielen', key='-PLAY-'), sg.Button('Pause', key='-PAUSE-'),
     sg.Button('Stopp', key='-STOP-')],
    [sg.Button('Hinzufügen'), sg.Button('Entfernen')],
    [sg.Text('Lautstärke'), sg.Slider((0,1), default_value=0.8, resolution=0.05, orientation='h', key='-VOL-', enable_events=True)],
    [sg.StatusBar('Gestoppt', key='-STATUS-')]
]
window = sg.Window('Audio Player', layout, finalize=True)
playlist = refresh_playlist(window)
current_idx = 0

while True:
    ev, vals = window.read(timeout=100)
    if ev in (sg.WINDOW_CLOSED, 'Exit'):
        break
    if ev == '-LIST-':
        sel = vals['-LIST-']
        if sel:
            current_idx = window['-LIST-'].get_indexes()[0]
    if ev == 'Hinzufügen':
        files = sg.popup_get_file('Datei auswählen', multiple_files=True, file_types=(('Audio','*.mp3;*.wav;*.ogg'),))
        if files:
            for f in files.split(';'):
                add_to_playlist(PLAYLIST_DB, f)
            playlist = refresh_playlist(window)
    if ev == 'Entfernen':
        if playlist:
            remove_from_playlist(PLAYLIST_DB, playlist[current_idx]['id'])
            playlist = refresh_playlist(window)
            current_idx = 0
    if ev == '-PLAY-':
        if playlist:
            res = player.play(playlist[current_idx]['file'])
            if res is not True:
                sg.popup_error(res)
    if ev == '-PAUSE-':
        player.toggle_pause()
    if ev == '-STOP-':
        player.stop()
    if ev == '-VOL-':
        player.set_volume(vals['-VOL-'])
    window['-STATUS-'].update(player.status())
window.close()
