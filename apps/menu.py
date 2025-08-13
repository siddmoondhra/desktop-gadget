from lib.display import Display
from lib.buttons import ButtonHandler
import time
import subprocess

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
        elif button == 'back':
            # Show shutdown confirmation
            self._show_shutdown_confirmation()
    
    def _show_shutdown_confirmation(self):
        """Show shutdown confirmation screen"""
        while True:
            self.display.draw_centered_text("Shutdown Pi?\nSELECT=Yes BACK=No")
            
            button = self.buttons.get_pressed()
            if button == 'select':
                # User confirmed shutdown
                self.display.draw_centered_text("Shutting down...\nGoodbye!")
                time.sleep(1)
                
                # Don't clear display - just shutdown
                self._shutdown_system()
                break
            elif button == 'back':
                # User cancelled shutdown
                return  # Go back to main menu
            
            time.sleep(0.1)
    
    def _clear_display_for_shutdown(self):
        """Simple display clear before shutdown"""
        try:
            # Just do a basic clear - don't try to be fancy
            self.display.clear()
        except Exception as e:
            print(f"Display clear error: {e}")
    
    def _shutdown_system(self):
        """Safely shutdown the system"""
        try:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'], check=True)
        except Exception as e:
            print(f"Shutdown failed: {e}")
            self.display.draw_centered_text("Shutdown failed!\nTry manually")