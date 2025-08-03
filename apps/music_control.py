import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyApp:
    def __init__(self, display, buttons):
        self.name = "Spotify"
        self.display = display
        self.buttons = buttons
        
        # DON'T authenticate in init - that's what's causing the startup issue
        self.auth_manager = None
        self.sp = None
        self.current_track = None
        self.is_playing = False
        
    def run(self):
        # Only set up Spotify when the app is actually run
        self.auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-playback-state,user-modify-playback-state",
            open_browser=False
        )
        
        # Initialize Spotify client - this will use cached token if available
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        
        while True:
            self._update_playback_state()
            self._display_playback_info()
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'select':
                self._toggle_playback()
            elif button == 'up':
                self._next_track()
            elif button == 'down':
                self._previous_track()
                
            time.sleep(0.1)
            
    def _clean_text(self, text):
        """Remove problematic Unicode characters"""
        if not text:
            return ""
        
        text = str(text)
        cleaned = ""
        for char in text:
            if ord(char) == 0xfe0f or ord(char) == 0xfe0e:
                continue
            if 0x200d <= ord(char) <= 0x200f:
                continue
            if 0x2060 <= ord(char) <= 0x206f:
                continue
            
            try:
                char.encode('latin-1')
                cleaned += char
            except UnicodeEncodeError:
                if char == '–':
                    cleaned += '-'
                elif char == '—':
                    cleaned += '-'
                elif char == ''':
                    cleaned += "'"
                elif char == ''':
                    cleaned += "'"
                elif char == '"':
                    cleaned += '"'
                elif char == '"':
                    cleaned += '"'
        
        return cleaned
        
    def _update_playback_state(self):
        try:
            current = self.sp.current_playback()
            if current:
                self.is_playing = current['is_playing']
                self.current_track = {
                    'name': self._clean_text(current['item']['name']),
                    'artist': self._clean_text(current['item']['artists'][0]['name'])
                }
        except Exception as e:
            print(f"Spotify error: {e}")
            self.current_track = None
            
    def _display_playback_info(self):
        if not self.current_track:
            self.display.draw_centered_text("No active playback")
            return
            
        status = "PLAY" if self.is_playing else "PAUSE"
        text = f"{status}\n{self.current_track['name']}\nby {self.current_track['artist']}"
        
        clean_text = self._clean_text(text)
        self.display.draw_centered_text(clean_text)
        
    def _toggle_playback(self):
        try:
            if self.is_playing:
                self.sp.pause_playback()
                self.is_playing = False
            else:
                try:
                    self.sp.start_playback()
                    self.is_playing = True
                except Exception as resume_error:
                    print(f"Resume failed, trying to find device: {resume_error}")
                    devices = self.sp.devices()
                    
                    if devices['devices']:
                        active_device = None
                        available_device = None
                        
                        for device in devices['devices']:
                            if device['is_active']:
                                active_device = device
                                break
                            elif available_device is None:
                                available_device = device
                        
                        target_device = active_device or available_device
                        
                        if target_device:
                            print(f"Trying device: {target_device['name']}")
                            self.sp.start_playback(device_id=target_device['id'])
                            self.is_playing = True
                        else:
                            raise Exception("No usable devices found")
                    else:
                        raise Exception("No devices available")
                        
        except Exception as e:
            print(f"Playback toggle error: {e}")
            if "No active device" in str(e) or "No devices" in str(e):
                self.display.draw_centered_text("Open Spotify app\nand play something")
            else:
                self.display.draw_centered_text("Playback error\nTry again")
            
    def _next_track(self):
        try:
            self.sp.next_track()
        except Exception as e:
            print(f"Next track error: {e}")
            
    def _previous_track(self):
        try:
            self.sp.previous_track()
        except Exception as e:
            print(f"Previous track error: {e}")