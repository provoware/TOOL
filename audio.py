import pygame, os
class AudioPlayer:
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.current_file = None
        self.is_paused = False
        self.volume = 0.8
    def load(self, file_path):
        """Load an audio file for playback."""
        if not os.path.isfile(file_path):
            return "Datei nicht gefunden!"
        try:
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            pygame.mixer.music.set_volume(self.volume)
            self.is_paused = False
            return True
        except Exception as e:
            return f"Fehler beim Laden: {e}"
    def play(self, file_path=None):
        """Play the current or a new audio file."""
        if file_path and file_path != self.current_file:
            result = self.load(file_path)
            if result is not True:
                return result
        try:
            pygame.mixer.music.play()
            self.is_paused = False
            return True
        except Exception as e:
            return f"Fehler beim Abspielen: {e}"
    def toggle_pause(self):
        """Pause or resume playback depending on the current state."""
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
            return True
        except Exception as e:
            return f"Fehler beim Pausieren: {e}"
    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.is_paused = False
            return True
        except Exception as e:
            return f"Fehler beim Stoppen: {e}"
    def set_volume(self, v):
        try:
            v = max(0, min(1, float(v)))
            pygame.mixer.music.set_volume(v)
            self.volume = v
            return True
        except Exception as e:
            return f"Fehler Lautstärke: {e}"
    def get_status(self):
        if self.is_paused:
            return "Pause"
        try:
            if pygame.mixer.music.get_busy():
                return "Abspielen"
        except Exception:
            pass
        return "Gestoppt"

    # Backwards compatible name used by the GUI
    def status(self):
        return self.get_status()
