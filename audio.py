import pygame, os
class AudioPlayer:
    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            pass
        self.current_file=None; self.is_paused=False; self.volume=0.8
    def load(self,file_path):
        if not os.path.isfile(file_path):
            return "Datei nicht gefunden!"
        try:
            pygame.mixer.music.load(file_path); self.current_file=file_path
            pygame.mixer.music.set_volume(self.volume); self.is_paused=False
            return True
        except Exception as e: return f"Fehler beim Laden: {e}"
    def play(self,file_path=None):
        if file_path and file_path!=self.current_file:
            r=self.load(file_path); 
            if r is not True: return r
        try: pygame.mixer.music.play(); self.is_paused=False; return True
        except Exception as e: return f"Fehler beim Abspielen: {e}"
    def pause(self):
        try:
            if self.is_paused: pygame.mixer.music.unpause(); self.is_paused=False
            else: pygame.mixer.music.pause(); self.is_paused=True
            return True
        except Exception as e: return f"Fehler beim Pausieren: {e}"
    def toggle_pause(self):
        try:
            if self.is_paused:
                pygame.mixer.music.unpause(); self.is_paused=False; return True
            else:
                return self.pause()
        except Exception as e: return f"Fehler beim Pausieren: {e}"
    def stop(self):
        try: pygame.mixer.music.stop(); self.is_paused=False; return True
        except Exception as e: return f"Fehler beim Stoppen: {e}"
    def set_volume(self,v):
        try: v=max(0,min(1,float(v))); pygame.mixer.music.set_volume(v); self.volume=v; return True
        except Exception as e: return f"Fehler Lautstärke: {e}"
    def get_status(self):
        status="Pause" if self.is_paused else "Gestoppt"
        try:
            if pygame.mixer.music.get_busy(): status="Abspielen"
        except: pass
        if self.current_file: status+=f" ({os.path.basename(self.current_file)})"
        return status
