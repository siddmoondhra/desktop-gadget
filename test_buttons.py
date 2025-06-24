import RPi.GPIO as GPIO
import time
import config

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup buttons with pull-ups
buttons = {
    'up': config.BUTTON_UP,
    'down': config.BUTTON_DOWN, 
    'select': config.BUTTON_SELECT,
    'back': config.BUTTON_BACK
}

for pin in buttons.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Button test - press buttons or Ctrl+C to exit")
print("Pin mapping:", buttons)

try:
    while True:
        for name, pin in buttons.items():
            if not GPIO.input(pin):  # Button pressed (LOW)
                print(f"Button {name} pressed (GPIO {pin})")
                time.sleep(0.3)  # Debounce
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\nTest finished")
    GPIO.cleanup()