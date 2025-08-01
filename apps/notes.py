import time

class NotesApp:
    def __init__(self, display, buttons):
        self.name = "Notes"
        self.display = display
        self.buttons = buttons
        self.notes = [
            "You got this bubba!",
            "I love you! <3",
            "You make me so happy",
            "I'm so proud of you",
            "You look amazing today!"
            "Thinking of you my love",
            "I miss you so, so much",
            "Rimsha, you mean the world to me :)",
            "I'll always love and support you!",
            "My love, you're the most:",
            "Loving,",
            "Hard-working,",
            "Funny,",
            "Beautiful,",
            "Caring,",
            "Gorgeous,",
            "Kind,",
            "Thoughtful,",
            "Passionate,",
            "And amazing person I know.",
            "You make every day special,",
            "and you're going to do great things :)"
            
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
