#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import config

# Test script to debug button issues
def test_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    button_pins = {
        'up': config.BUTTON_UP,      # 17
        'down': config.BUTTON_DOWN,  # 27
        'select': config.BUTTON_SELECT, # 22
        'back': config.BUTTON_BACK   # 23
    }
    
    # Setup buttons
    for name, pin in button_pins.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"Button {name} on pin {pin}")
    
    print("Button test started. Press buttons to test...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            for name, pin in button_pins.items():
                # Read raw pin state
                pin_state = GPIO.input(pin)
                if not pin_state:  # Button pressed (LOW due to pull-up)
                    print(f"Button {name} (pin {pin}) is pressed! Raw state: {pin_state}")
                    time.sleep(0.5)  # Prevent spam
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nTest ended")
        GPIO.cleanup()

if __name__ == "__main__":
    test_buttons()