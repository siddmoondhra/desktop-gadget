from apps.menu import Menu
from apps.weather import WeatherApp
from apps.notes import NotesApp
from apps.spotify import SpotifyApp
from apps.timer import TimerApp
from lib.display import Display
from lib.buttons import ButtonHandler
import board
import busio


def main():
    # Initialize hardware
    i2c = busio.I2C(board.SCL, board.SDA)
    display = Display(i2c, OLED_WIDTH, OLED_HEIGHT, OLED_ADDRESS)
    buttons = ButtonHandler(config)
    
    # Initialize apps
    apps = [
        WeatherApp(display, buttons),
        NotesApp(display, buttons),
        # Add other apps here
    ]
    
    # Start menu system
    menu = Menu(display, buttons, apps)
    menu.run()

if __name__ == "__main__":
    main()