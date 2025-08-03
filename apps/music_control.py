import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyApp:
    def __init__(self, display, buttons):
        self.name = "Spotify"
        self.display = display
        self.buttons = buttons
        self.sp = None
        self.current_track = None
        self.is_playing = False
        
    def run(self):
        # Try to use existing token or create new one
        if not self._setup_spotify():
            return
            
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
            
    def _setup_spotify(self):
        """Setup Spotify client using the simplest method possible"""
        try:
            # Method 1: Try using cached token
            auth_manager = SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope="user-read-playback-state,user-modify-playback-state",
                open_browser=False,
                cache_path=".cache"
            )
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test if it works
            self.sp.current_user()
            print("Using cached authentication")
            return True
            
        except Exception as e:
            print(f"Cached auth failed: {e}")
            
        # Method 2: Manual token creation
        print("\nManual Setup Required:")
        print("1. Go to: https://developer.spotify.com/console/get-current-user/")
        print("2. Click 'Get Token'")
        print("3. Select the required scopes:")
        print("   - user-read-playback-state")
        print("   - user-modify-playback-state")
        print("4. Copy the token that appears")
        
        token = input("\nPaste your token here: ").strip()
        
        try:
            self.sp = spotipy.Spotify(auth=token)
            # Test the token
            self.sp.current_user()
            print("Token works!")
            
            # Save token for future use
            import json
            token_data = {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "user-read-playback-state user-modify-playback-state"
            }
            
            with open('.cache-manual', 'w') as f:
                json.dump(token_data, f)
                
            return True
            
        except Exception as e:
            print(f"Token failed: {e}")
            self.display.draw_centered_text("Setup failed")
            time.sleep(2)
            return False
            
    def _clean_text(self, text):
        """Remove problematic characters"""
        if not text:
            return ""
        
        cleaned = ""
        for char in str(text):
            try:
                char.encode('ascii')
                cleaned += char
            except UnicodeEncodeError:
                if char in ['–', '—']:
                    cleaned += '-'
                elif char in [''', ''']:
                    cleaned += "'"
                elif char in ['"', '"']:
                    cleaned += '"'
        
        return cleaned
        
    def _update_playback_state(self):
        try:
            current = self.sp.current_playback()
            if current and current.get('item'):
                self.is_playing = current['is_playing']
                self.current_track = {
                    'name': self._clean_text(current['item']['name']),
                    'artist': self._clean_text(current['item']['artists'][0]['name'])
                }
            else:
                self.current_track = None
        except Exception:
            self.current_track = None
            
    def _display_playback_info(self):
        if not self.current_track:
            self.display.draw_centered_text("No music\nplaying")
            return
            
        status = "PLAYING" if self.is_playing else "PAUSED"
        text = f"{status}\n{self.current_track['name']}\n{self.current_track['artist']}"
        
        self.display.draw_centered_text(text)
        
    def _toggle_playback(self):
        try:
            if self.is_playing:
                self.sp.pause_playback()
            else:
                self.sp.start_playback()
        except Exception as e:
            if "No active device" in str(e):
                self.display.draw_centered_text("Start Spotify\nfirst")
            else:
                self.display.draw_centered_text("Error")
            time.sleep(1)
            
    def _next_track(self):
        try:
            self.sp.next_track()
        except Exception:
            pass
            
    def _previous_track(self):
        try:
            self.sp.previous_track()
        except Exception:
            pass