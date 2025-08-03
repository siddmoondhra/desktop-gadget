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
        
        self.sp = None
        self.current_track = None
        self.is_playing = False
        
    def run(self):
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
            print(f"\nNote: The URL will start with 'http://127.0.0.1:8888/callback?code=...'")
            print(f"It's normal if the page shows an error - just copy the URL!")
            print("-" * 50)
            
            # Get the redirect response
            redirect_response = input("Paste the redirect URL here: ").strip()
            
            try:
                # Get the access token
                token_info = self.auth_manager.get_access_token(redirect_response)
                print("Authentication successful!")
                time.sleep(2)
            except Exception as e:
                print(f"Authentication failed: {e}")
                print("Please try running the app again.")
                return
        
        # Initialize Spotify client
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
                
            time.sleep(0.1)  # Much faster response - was 0.5
            
    def _clean_text(self, text):
        """Remove problematic Unicode characters"""
        if not text:
            return ""
        
        text = str(text)
        
        # Remove variation selectors and other invisible Unicode characters
        cleaned = ""
        for char in text:
            # Skip variation selectors and other problematic Unicode ranges
            if ord(char) == 0xfe0f:  # Variation selector-16
                continue
            if ord(char) == 0xfe0e:  # Variation selector-15
                continue
            if 0x200d <= ord(char) <= 0x200f:  # Zero-width joiners
                continue
            if 0x2060 <= ord(char) <= 0x206f:  # Various invisible characters
                continue
            
            try:
                # Test if character can be encoded to latin-1
                char.encode('latin-1')
                cleaned += char
            except UnicodeEncodeError:
                # Replace with ASCII equivalent if possible
                if char == '–':  # en dash
                    cleaned += '-'
                elif char == '—':  # em dash
                    cleaned += '-'
                elif char == ''':  # left single quote
                    cleaned += "'"
                elif char == ''':  # right single quote
                    cleaned += "'"
                elif char == '"':  # left double quote
                    cleaned += '"'
                elif char == '"':  # right double quote
                    cleaned += '"'
                else:
                    # Skip unknown characters
                    pass
        
        return cleaned
        
    def _update_playback_state(self):
        try:
            current = self.sp.current_playback()
            if current:
                self.is_playing = current['is_playing']
                # Clean the text data from Spotify
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
            
        # Use simple ASCII characters only
        status = "PLAY" if self.is_playing else "PAUSE"
        text = f"{status}\n{self.current_track['name']}\nby {self.current_track['artist']}"
        
        # Clean the final text as well
        clean_text = self._clean_text(text)
        
        self.display.draw_centered_text(clean_text)
        
    def _toggle_playback(self):
        try:
            if self.is_playing:
                self.sp.pause_playback()
                self.is_playing = False
            else:
                # Try to resume playback
                try:
                    self.sp.start_playback()
                    self.is_playing = True
                except Exception as resume_error:
                    # If resume fails, try to find and activate a device
                    print(f"Resume failed, trying to find device: {resume_error}")
                    devices = self.sp.devices()
                    
                    if devices['devices']:
                        # Find the best device (prefer active ones)
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
            # Show helpful error message
            if "No active device" in str(e) or "No devices" in str(e):
                self.display.draw_centered_text("Open Spotify app\nand play something")
            else:
                self.display.draw_centered_text("Playback error\nTry again")
            
    def _next_track(self):
        try:
            self.sp.next_track()
            # Remove the sleep - let the next update cycle handle it
        except Exception as e:
            print(f"Next track error: {e}")
            
    def _previous_track(self):
        try:
            self.sp.previous_track()
            # Remove the sleep - let the next update cycle handle it
        except Exception as e:
            print(f"Previous track error: {e}")