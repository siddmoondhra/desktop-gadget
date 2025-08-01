# Makes the apps directory a Python package
from .menu import Menu
from .weather import WeatherApp
from .notes import NotesApp
from .music_control import SpotifyApp
from .timer import TimerApp
from .games_menu import GamesMenu
from .snake_game import SnakeGame
from .dino_game import DinoRunner

__all__ = ['Menu', 'WeatherApp', 'NotesApp', 'SpotifyApp', 'TimerApp', 'GamesMenu', 'SnakeGame', 'DinoRunner']