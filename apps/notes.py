import time

class NotesApp:
    def __init__(self, display, buttons):
        self.name = "Sweet Notes"
        self.display = display
        self.buttons = buttons
        self.notes = [
            "You're amazing! ❤️",
            "I love you!",
            "You make me happy",
            "You're my sunshine ☀️",
            "Thinking of you 💭"
        ]
        self.current_note = 0
        
    def run(self):
        while True:
            self.display.draw_centered_text(self.notes[self.current_note])
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'up':
                self.current_note = (self.current_note - 1) % len(self.notes)
                time.sleep(0.2)  # debounce
            elif button == 'down':
                self.current_note = (self.current_note + 1) % len(self.notes)
                time.sleep(0.2)
            elif button == 'select':
                # Could implement adding new notes here
                pass
                
            time.sleep(0.1)
