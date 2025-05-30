from display import show_message
from buttons import wait_for_button
from weather import get_weather
import time

def main():
    while True:
        message = "Hello, love!"
        show_message(message)
        weather = get_weather()
        show_message(f"Weather: {weather}")
        wait_for_button()
        time.sleep(1)

if __name__ == "__main__":
    main()
