import time

class GamesMenu:
    def __init__(self, display, buttons, games):
        self.name = "Games"
        self.display = display
        self.buttons = buttons
        self.games = games
        self.selected_index = 0
        self.current_game = None
        
    def run(self):
        while True:
            if self.current_game is None:
                self._show_games_menu()
                button = self.buttons.get_pressed()
                if self._handle_games_menu_input(button):
                    return  # Return to main menu
            else:
                # Run the current game
                self.current_game.run()
                self.current_game = None  # Return to games menu when game exits
                
    def _show_games_menu(self):
        game_name = self.games[self.selected_index].name
        # Show "Games:" prefix to indicate we're in the games submenu
        self.display.draw_centered_text(f"{game_name}")
        
    def _handle_games_menu_input(self, button):
        if button == 'up':
            self.selected_index = (self.selected_index - 1) % len(self.games)
        elif button == 'down':
            self.selected_index = (self.selected_index + 1) % len(self.games)
        elif button == 'select':
            self.current_game = self.games[self.selected_index]
        elif button == 'back':
            return True  # Signal to return to main menu
        return False