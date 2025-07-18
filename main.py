import board
import busio
import time
from apps.menu import Menu
from apps.weather import WeatherApp
from apps.notes import NotesApp
from apps.music_control import SpotifyApp
from apps.timer import TimerApp
from apps.snake_game import SnakeGame  # Add this import
from apps.dino_runner import DinoRunner  # Add this import
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
        
        # Initialize apps (including games)
        apps = [
            WeatherApp(display, buttons),
            NotesApp(display, buttons),
            SpotifyApp(display, buttons),
            TimerApp(display, buttons),
            SnakeGame(display, buttons),      # Add Snake game
            DinoRunner(display, buttons)      # Add Dino Runner game
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