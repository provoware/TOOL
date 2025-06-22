import os
import pygame


class AudioPlayer:
    """Simple wrapper around ``pygame.mixer`` for playing audio files."""

    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception:
            # ``pygame`` might fail to initialise if no audio device is
            # available. We silently ignore this so the rest of the
            # application can still run.
            pass
        self.current_file: str | None = None
        self.is_paused: bool = False
        self.volume: float = 0.8

    def load(self, file_path: str):
        if not os.path.isfile(file_path):
            return "Datei nicht gefunden!"
        try:
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            pygame.mixer.music.set_volume(self.volume)
            self.is_paused = False
            return True
        except Exception as exc:  # pragma: no cover - thin wrapper
            return f"Fehler beim Laden: {exc}"

    def play(self, file_path: str | None = None):
        if file_path and file_path != self.current_file:
            res = self.load(file_path)
            if res is not True:
                return res
        try:
            pygame.mixer.music.play()
            self.is_paused = False
            return True
        except Exception as exc:  # pragma: no cover - thin wrapper
            return f"Fehler beim Abspielen: {exc}"

    def toggle_pause(self):
        """Toggle between pause and unpause."""
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
            return True
        except Exception as exc:  # pragma: no cover - thin wrapper
            return f"Fehler beim Pausieren: {exc}"

    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.is_paused = False
            return True
        except Exception as exc:  # pragma: no cover - thin wrapper
            return f"Fehler beim Stoppen: {exc}"

    def set_volume(self, volume: float):
        try:
            volume = max(0.0, min(1.0, float(volume)))
            pygame.mixer.music.set_volume(volume)
            self.volume = volume
            return True
        except Exception as exc:  # pragma: no cover - thin wrapper
            return f"Fehler Lautstärke: {exc}"

    def status(self) -> str:
        if self.is_paused:
            return "Pause"
        try:
            if pygame.mixer.music.get_busy():
                return "Abspielen"
        except Exception:  # pragma: no cover - depends on mixer
            pass
        return "Gestoppt"
