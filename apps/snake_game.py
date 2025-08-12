import time
import random
from PIL import Image, ImageDraw

class SnakeGame:
    def __init__(self, display, buttons):
        self.name = "Snake"
        self.display = display
        self.buttons = buttons
        
        # Game settings
        self.grid_size = 4  # 4x4 pixel blocks
        self.game_width = self.display.width // self.grid_size  # 32 blocks wide
        self.game_height = self.display.height // self.grid_size  # 8 blocks tall
        
        # Game state
        self.snake = [(self.game_width // 2, self.game_height // 2)]
        self.direction = (1, 0)  # Moving right initially
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False
        self.speed = 0.3  # Seconds between moves
        
        # Back button handling for double-press exit
        self.back_press_count = 0
        self.last_back_press = 0
        self.double_press_window = 0.5  # 0.5 seconds to register double press
        
        # Direction buffering for rapid inputs
        self.queued_direction = None
        
    def run(self):
        self._reset_game()
        last_move_time = time.time()
        
        while True:
            current_time = time.time()
            
            # Handle input
            button = self.buttons.get_pressed()
            if button == 'back':
                # Handle double-press exit logic without changing direction
                if current_time - self.last_back_press < self.double_press_window:
                    return
                else:
                    self.last_back_press = current_time
            elif button == 'select' and self.game_over:
                self._reset_game()
                last_move_time = time.time()
                continue
            elif not self.game_over:
                if button in ['up', 'down', 'left', 'right']:
                    # Absolute direction mapping
                    mapping = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
                    new_direction = mapping[button]
                    # Determine effective current direction
                    effective_direction = self.queued_direction if self.queued_direction is not None else self.direction
                    if new_direction != (-effective_direction[0], -effective_direction[1]):
                        self.queued_direction = new_direction
                elif button == 'select':
                    # Turbo: process queued direction if any and move immediately
                    if self.queued_direction is not None:
                        self.direction = self.queued_direction
                        self.queued_direction = None
                    self._move_snake()
                    last_move_time = current_time
            
            # Automatic move based on timer
            if not self.game_over and current_time - last_move_time >= self.speed:
                if self.queued_direction is not None:
                    self.direction = self.queued_direction
                    self.queued_direction = None
                self._move_snake()
                last_move_time = current_time
                
            # Draw game
            self._draw_game()
            time.sleep(0.01)  # Faster loop for rapid input
            
    def _reset_game(self):
        self.snake = [(self.game_width // 2, self.game_height // 2)]
        self.direction = (1, 0)
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False
        self.back_press_count = 0
        self.last_back_press = 0
        self.queued_direction = None
        
    def _generate_food(self):
        while True:
            food_pos = (random.randint(0, self.game_width - 1), 
                       random.randint(0, self.game_height - 1))
            if food_pos not in self.snake:
                return food_pos
                
    def _move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.game_width or 
            new_head[1] < 0 or new_head[1] >= self.game_height):
            self.game_over = True
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food()
            # Increase speed slightly
            self.speed = max(0.1, self.speed - 0.01)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
    def _draw_game(self):
        try:
            image = Image.new("1", (self.display.width, self.display.height))
            draw = ImageDraw.Draw(image)
            
            if self.game_over:
                # Game over screen
                self.display.draw_centered_text(f"Game Over!\nScore: {self.score}\nPress SELECT")
                return
                
            # Draw snake
            for segment in self.snake:
                x = segment[0] * self.grid_size
                y = segment[1] * self.grid_size
                draw.rectangle([x, y, x + self.grid_size - 1, y + self.grid_size - 1], 
                             fill=255)
                
            # Draw food (blinking effect)
            if int(time.time() * 3) % 2:  # Blink every ~0.33 seconds
                fx = self.food[0] * self.grid_size
                fy = self.food[1] * self.grid_size
                draw.rectangle([fx, fy, fx + self.grid_size - 1, fy + self.grid_size - 1], 
                             fill=255)
                
            # Draw score in top-left corner
            draw.text((0, 0), str(self.score), fill=255)
            
            self.display.oled.image(image)
            self.display.oled.show()
            
        except Exception as e:
            print(f"Snake game draw error: {e}")
            self.display.draw_centered_text(f"Draw error:\n{str(e)[:15]}")