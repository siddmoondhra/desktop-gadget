import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyApp:
    def __init__(self, display, buttons):
        self.name = "Spotify"
        self.display = display
        self.buttons = buttons
        
        # Spotify setup with manual authentication
        self.auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-playback-state,user-modify-playback-state",
            open_browser=False  # Prevent automatic browser opening
        )
        
        # Check if we need to authenticate
        token_info = self.auth_manager.get_cached_token()
        if not token_info:
            print("\n" + "="*50)
            print("SPOTIFY AUTHENTICATION REQUIRED")
            print("="*50)
            
            # Get the authorization URL
            auth_url = self.auth_manager.get_authorize_url()
            print(f"\n1. Go to this URL in a browser (phone/computer):")
            print(f"{auth_url}")
            print(f"\n2. Log in with your girlfriend's Spotify account")
            print(f"3. After logging in, copy the FULL URL from the address bar")
            print(f"4. Paste it below and press Enter")
            print(f"\nNote: The URL will start with 'http://localhost:8080/?code=...'")
            print(f"It's normal if the page shows an error - just copy the URL!")
            print("-" * 50)
            
            # Get the redirect response
            redirect_response = input("Paste the redirect URL here: ").strip()
            
            try:
                # Get the access token
                token_info = self.auth_manager.get_access_token(redirect_response)
                print("✅ Authentication successful!")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                print("Please try running the app again.")
                raise
        
        # Initialize Spotify client
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
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