from lib.display import Display
from lib.buttons import ButtonHandler
import time

class Menu:
    def __init__(self, display, buttons, apps):
        self.display = display
        self.buttons = buttons
        self.apps = apps
        self.selected_index = 0
        self.current_app = None
        
    def run(self):
        while True:
            if self.current_app is None:
                self._show_menu()
                button = self.buttons.get_pressed()
                self._handle_menu_input(button)
            else:
                # Run the current app
                self.current_app.run()
                self.current_app = None  # Return to menu when app exits
                
    def _show_menu(self):
        self.display.draw_centered_text(self.apps[self.selected_index].name)
        
    def _handle_menu_input(self, button):
        if button == 'up':
            self.selected_index = (self.selected_index - 1) % len(self.apps)
        elif button == 'down':
            self.selected_index = (self.selected_index + 1) % len(self.apps)
        elif button == 'select':
            self.current_app = self.apps[self.selected_index]