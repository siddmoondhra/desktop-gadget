import RPi.GPIO as GPIO
import time

class ButtonHandler:
    def __init__(self, config):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.button_pins = {
            'up': config.BUTTON_UP,
            'down': config.BUTTON_DOWN,
            'select': config.BUTTON_SELECT,
            'back': config.BUTTON_BACK
        }
        
        # Setup buttons with pull-up resistors
        for pin in self.button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.last_press_time = {}
        self.debounce_delay = 0.2
        
    def get_pressed(self):
        current_time = time.time()
        
        for name, pin in self.button_pins.items():
            # Button is pressed when pin reads LOW (due to pull-up)
            if not GPIO.input(pin):
                # Check debounce
                if name not in self.last_press_time or \
                   (current_time - self.last_press_time[name]) > self.debounce_delay:
                    self.last_press_time[name] = current_time
                    return name
        return None
    
    def cleanup(self):
        GPIO.cleanup()