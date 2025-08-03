import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse

class SpotifyApp:
    def __init__(self, display, buttons):
        self.name = "Spotify"
        self.display = display
        self.buttons = buttons
        
        # Don't authenticate during init - wait until the app is run
        self.auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-playback-state,user-modify-playback-state",
            open_browser=False
        )
        
        self.sp = None
        self.current_track = None
        self.is_playing = False
        
    def _authenticate(self):
        """Handle Spotify authentication using Device Flow (no redirect URI needed)"""
        # Check if we already have a token
        token_info = self.auth_manager.get_cached_token()
        if token_info:
            return True
            
        self.display.draw_centered_text("Spotify Auth\nRequired")
        time.sleep(2)
        
        print("\n" + "="*50)
        print("SPOTIFY DEVICE AUTHENTICATION")
        print("="*50)
        
        try:
            # Use device flow instead of authorization code flow
            import requests
            
            # Get device code
            device_auth_url = "https://accounts.spotify.com/api/token"
            device_code_data = {
                'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
                'scope': 'user-read-playback-state user-modify-playback-state'
            }
            
            # Request device code
            device_response = requests.post(
                "https://accounts.spotify.com/api/device-authorization",
                data=device_code_data
            )
            
            if device_response.status_code == 200:
                device_data = device_response.json()
                
                print(f"\n1. Go to: {device_data['verification_uri']}")
                print(f"2. Enter this code: {device_data['user_code']}")
                print(f"3. Log in with your girlfriend's Spotify account")
                print(f"4. Press Enter here when done")
                print("-" * 50)
                
                self.display.draw_centered_text(f"Go to:\nspotify.com/pair\nCode: {device_data['user_code']}")
                
                input("Press Enter after completing authentication...")
                
                # Poll for token
                token_data = {
                    'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
                    'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
                    'device_code': device_data['device_code'],
                    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
                }
                
                for attempt in range(30):  # Try for 5 minutes
                    token_response = requests.post(device_auth_url, data=token_data)
                    
                    if token_response.status_code == 200:
                        token_info = token_response.json()
                        
                        # Save token manually since we're not using the normal flow
                        import json
                        with open('.cache', 'w') as f:
                            json.dump(token_info, f)
                        
                        print("✅ Authentication successful!")
                        return True
                    elif token_response.status_code == 400:
                        error = token_response.json()
                        if error.get('error') == 'authorization_pending':
                            time.sleep(device_data['interval'])
                            continue
                        else:
                            raise Exception(f"Auth error: {error}")
                    else:
                        time.sleep(device_data['interval'])
                
                raise Exception("Authentication timed out")
            else:
                raise Exception(f"Failed to get device code: {device_response.status_code}")
                
        except Exception as e:
            print(f"❌ Device authentication failed: {e}")
            self.display.draw_centered_text("Auth failed\nTry again")
            time.sleep(3)
            return False
        
    def _clean_text(self, text):
        """Remove problematic Unicode characters"""
        if not text:
            return ""
        
        # Convert to string and remove variation selectors and other problematic Unicode
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
        
    def run(self):
        # Authenticate when the app is actually run
        if not self._authenticate():
            return  # Exit if authentication failed
            
        # Initialize Spotify client after successful authentication
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