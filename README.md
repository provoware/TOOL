# SongArchiv Release v4.0.3-r3

This repository contains a lightweight demo of a simple audio player using
`PySimpleGUI` and `pygame`.  The code is intentionally small and is aimed at
showing the basic project structure.  To get the application running use the
following steps:

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the GUI:

   ```bash
   python main.py
   ```

Audio files can be added to the playlist via the GUI.  The application keeps a
small SQLite database in the `db/` folder.
