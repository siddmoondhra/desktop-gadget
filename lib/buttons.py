import digitalio
import board
import time

class ButtonHandler:
    def __init__(self, config):
        self.buttons = {
            'up': self._setup_button(config.BUTTON_UP),
            'down': self._setup_button(config.BUTTON_DOWN),
            'select': self._setup_button(config.BUTTON_SELECT),
            'back': self._setup_button(config.BUTTON_BACK)
        }
        
    def _setup_button(self, pin):
        button = digitalio.DigitalInOut(getattr(board, f"D{pin}"))
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP  
        
    def get_pressed(self):
        for name, button in self.buttons.items():
            if not button.value:  
                time.sleep(0.1)  # debounce
                return name
        return None