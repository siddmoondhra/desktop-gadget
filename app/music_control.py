import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state user-modify-playback-state"

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope=scope
))

def get_current_playing():
    current = sp.current_playback()
    if not current or not current.get("item"):
        return "No music playing"
    name = current["item"]["name"]
    artist = current["item"]["artists"][0]["name"]
    return f"{name} - {artist}"

def pause():
    sp.pause_playback()

def play():
    sp.start_playback()

def next_track():
    sp.next_track()

def previous_track():
    sp.previous_track()
