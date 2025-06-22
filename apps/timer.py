import time

class TimerApp:
    def __init__(self, display, buttons):
        self.name = "Timer"
        self.display = display
        self.buttons = buttons
        self.running = False
        self.start_time = 0
        self.duration = 300  # 5 minutes default
        self.saved_durations = [60, 300, 600, 1800]  # 1, 5, 10, 30 minutes
        
    def run(self):
        self._reset_timer()
        while True:
            self._update_display()
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'select':
                self._toggle_timer()
            elif button == 'up':
                self._increase_duration()
            elif button == 'down':
                self._decrease_duration()
                
            time.sleep(0.1)
            
    def _update_display(self):
        if self.running:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.duration - elapsed)
            if remaining <= 0:
                self.display.draw_centered_text("TIME'S UP!\nPress back")
                return
        else:
            remaining = self.duration
            
        mins, secs = divmod(int(remaining), 60)
        timer_text = f"{mins:02d}:{secs:02d}"
        status = "▶️" if self.running else "⏸️"
        self.display.draw_centered_text(f"{status} {timer_text}\nSet: {self.duration//60}min")
        
    def _toggle_timer(self):
        if self.running:
            self.running = False
        else:
            if self.duration <= 0:
                self.duration = 300  # Reset to 5 minutes if 0
            self.start_time = time.time()
            self.running = True
            
    def _increase_duration(self):
        if not self.running:
            # Find next saved duration
            for d in sorted(self.saved_durations):
                if d > self.duration:
                    self.duration = d
                    return
            self.duration = self.saved_durations[0]  # Wrap around
            
    def _decrease_duration(self):
        if not self.running:
            # Find previous saved duration
            for d in sorted(self.saved_durations, reverse=True):
                if d < self.duration:
                    self.duration = d
                    return
            self.duration = self.saved_durations[-1]  # Wrap around
            
    def _reset_timer(self):
        self.running = False
        self.start_time = 0