# Makes the apps directory a Python package
from .menu import Menu
from .weather import WeatherApp
from .notes import NotesApp
from .music_control import SpotifyApp
from .timer import TimerApp

__all__ = ['Menu', 'WeatherApp', 'NotesApp', 'SpotifyApp', 'TimerApp']