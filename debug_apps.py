from apps.menu import Menu
from apps.weather import WeatherApp
from apps.notes import NotesApp
from apps.timer import TimerApp
from lib.display import Display
from lib.buttons import ButtonHandler
import board
import busio
import config
import time

# Initialize hardware
i2c = busio.I2C(board.SCL, board.SDA)
display = Display(i2c, config.OLED_WIDTH, config.OLED_HEIGHT, config.OLED_ADDRESS)
buttons = ButtonHandler(config)

# Test each app individually
print("Testing Notes app...")
try:
    notes_app = NotesApp(display, buttons)
    print("Notes app created successfully")
    # Run for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        button = buttons.get_pressed()
        if button == 'back':
            break
        elif button == 'up':
            notes_app.current_note = (notes_app.current_note - 1) % len(notes_app.notes)
        elif button == 'down':
            notes_app.current_note = (notes_app.current_note + 1) % len(notes_app.notes)
        
        display.draw_centered_text(notes_app.notes[notes_app.current_note])
        time.sleep(0.1)
    
    print("Notes app test completed")
except Exception as e:
    print(f"Notes app error: {e}")

print("\nTesting Timer app...")
try:
    timer_app = TimerApp(display, buttons)
    print("Timer app created successfully")
    # Run for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        button = buttons.get_pressed()
        if button == 'back':
            break
        
        mins, secs = divmod(int(timer_app.duration), 60)
        timer_text = f"{mins:02d}:{secs:02d}"
        display.draw_centered_text(f"Timer Test\n{timer_text}")
        time.sleep(0.1)
    
    print("Timer app test completed")
except Exception as e:
    print(f"Timer app error: {e}")

print("Debug test finished")