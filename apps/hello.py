import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class HelloScreen:
    def __init__(self, display, buttons):
        self.display = display
        self.buttons = buttons
        self.last_update = 0
        
    def show(self):
        """Display the hello screen with date/time and wait for any button press"""
        while True:
            current_time = time.time()
            
            # Update display every second to show current time
            if current_time - self.last_update >= 1:
                self._update_display()
                self.last_update = current_time
            
            # Check for any button press
            button = self.buttons.get_pressed()
            if button:  # Any button press will exit
                # Optional: show a quick transition message
                self.display.draw_centered_text("Starting...")
                time.sleep(0.5)
                return
            
            time.sleep(0.1)  # Small delay to prevent CPU spinning
    
    def _update_display(self):
        """Update the display with current date and time"""
        # Get current time in EST/EDT
        now = datetime.now(timezone.utc).astimezone(ZoneInfo("America/New_York"))

        # Format the date and time
        date_str = now.strftime("%b %d, %Y")  # e.g., "Jan 15, 2025"
        time_str = now.strftime("%I:%M:%S %p")  # e.g., "03:45:20 PM"

        # Create the display message (date and time only)
        hello_messages = [
            f"{date_str}",
            f"{time_str} ET"  # Using ET to cover both EST and EDT
        ]

        # Display the message
        hello_text = "\n".join(hello_messages)
        self.display.draw_centered_text(hello_text)