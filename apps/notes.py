import time

class NotesApp:
    def __init__(self, display, buttons):
        self.name = "Notes"
        self.display = display
        self.buttons = buttons
        self.notes = [
            "I've put some motivational blurbs here,",
            "Kinda like fortune cookies,",
            "I'll change them periodically",
            "and I hope you like it!",
            "Believe in yourself, you got this!",
            "You deserve great things",
            "You're doing awesome Rimsha!",
            "Lock in and achieve your goals",
            "Take it one task at a time",
            "You're more capable than you realize",
            "Don't forget to hydrate :)"
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
