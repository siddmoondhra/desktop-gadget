import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyApp:
    def __init__(self, display, buttons):
        self.name = "Spotify"
        self.display = display
        self.buttons = buttons
        
        # Spotify setup
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-playback-state,user-modify-playback-state"))
            
        self.current_track = None
        self.is_playing = False
        
    def run(self):
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
                
            time.sleep(0.5)  # Longer sleep to reduce API calls
            
    def _update_playback_state(self):
        try:
            current = self.sp.current_playback()
            if current:
                self.is_playing = current['is_playing']
                self.current_track = {
                    'name': current['item']['name'],
                    'artist': current['item']['artists'][0]['name']
                }
        except Exception as e:
            print(f"Spotify error: {e}")
            self.current_track = None
            
    def _display_playback_info(self):
        if not self.current_track:
            self.display.draw_centered_text("No active playback")
            return
            
        status = "▶️" if self.is_playing else "⏸️"
        text = f"{status} {self.current_track['name']}\nby {self.current_track['artist']}"
        self.display.draw_centered_text(text)
        
    def _toggle_playback(self):
        try:
            if self.is_playing:
                self.sp.pause_playback()
            else:
                self.sp.start_playback()
            self.is_playing = not self.is_playing
        except Exception as e:
            print(f"Playback toggle error: {e}")
            
    def _next_track(self):
        try:
            self.sp.next_track()
            time.sleep(0.5)  # Wait for update
        except Exception as e:
            print(f"Next track error: {e}")
            
    def _previous_track(self):
        try:
            self.sp.previous_track()
            time.sleep(0.5)  # Wait for update
        except Exception as e:
            print(f"Previous track error: {e}")