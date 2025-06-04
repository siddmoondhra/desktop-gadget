# main.py
from app.music_control import get_current_playing
from app.display import show_text

song_info = get_current_playing()
lines = [line.strip() for line in song_info.split(" - ")]
show_text(lines)
