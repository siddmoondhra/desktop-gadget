import board
import busio
import time
from apps.menu import Menu
from apps.weather import WeatherApp
from apps.notes import NotesApp
from apps.music_control import SpotifyApp
from apps.timer import TimerApp
from apps.snake_game import SnakeGame  # Your existing snake game
from apps.dino_game import DinoRunner  # Your existing dino game
from apps.games_menu import GamesMenu  # New games menu
from lib.display import Display
from lib.buttons import ButtonHandler
import config

def main():
    try:
        # Initialize hardware
        i2c = busio.I2C(board.SCL, board.SDA)
        display = Display(i2c, config.OLED_WIDTH, config.OLED_HEIGHT, config.OLED_ADDRESS)
        buttons = ButtonHandler(config)
        
        # Show startup message
        display.draw_centered_text("Starting up...")
        time.sleep(1)
        
        # Initialize games separately
        games = [
            SnakeGame(display, buttons),
            DinoRunner(display, buttons)
        ]
        
        # Create games menu
        games_menu = GamesMenu(display, buttons, games)
        
        # Initialize main apps (including games menu)
        apps = [
            WeatherApp(display, buttons),
            NotesApp(display, buttons),
            SpotifyApp(display, buttons),
            TimerApp(display, buttons),
            games_menu  # Games submenu replaces individual games
        ]
        
        # Start menu system
        menu = Menu(display, buttons, apps)
        menu.run()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        display.clear()
        buttons.cleanup()  # Clean up GPIO
    except Exception as e:
        print(f"Error: {e}")
        if 'display' in locals():
            display.draw_centered_text(f"Error:\n{str(e)[:20]}")
            time.sleep(3)
        if 'buttons' in locals():
            buttons.cleanup()

if __name__ == "__main__":
    main()