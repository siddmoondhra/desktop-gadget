import RPi.GPIO as GPIO
import time

# Your actual pin mapping
buttons = {
    'up': 17,      # Grey wire, Pin 11
    'down': 27,    # Black wire, Pin 13  
    'select': 22,  # Brown wire, Pin 15
    'back': 23     # Purple wire, Pin 16
}

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setup all pins
for name, pin in buttons.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Testing buttons with your exact wiring:")
print("Grey (up), Black (down), Brown (select), Purple (back)")

try:
    while True:
        for name, pin in buttons.items():
            if not GPIO.input(pin):
                print(f"{name} button pressed (GPIO {pin})")
                time.sleep(0.3)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Test finished")
    GPIO.cleanup()