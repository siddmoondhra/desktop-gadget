import time
import random
from PIL import Image, ImageDraw

class DinoRunner:
    def __init__(self, display, buttons):
        self.name = "Dino Runner"
        self.display = display
        self.buttons = buttons
        
        # Game settings
        self.ground_height = 6
        self.dino_width = 6
        self.dino_height = 8
        self.obstacle_width = 3
        self.obstacle_height = 8
        
        # Game state
        self.dino_x = 15
        self.dino_y = self.display.height - self.ground_height - self.dino_height
        self.dino_velocity = 0
        self.dino_on_ground = True
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.speed = 2  # Pixels per frame
        self.jump_power = -6
        self.gravity = 0.8
        
        # Animation
        self.frame_count = 0
        self.spawn_timer = 0
        self.spawn_interval = 60  # Frames between obstacles
        
    def run(self):
        self._reset_game()
        
        while True:
            # Handle input
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'select':
                if self.game_over:
                    self._reset_game()
                    continue
                elif self.dino_on_ground:
                    self._jump()
            elif button == 'down' and not self.dino_on_ground:
                # Fast fall
                self.dino_velocity += 2
                
            if not self.game_over:
                self._update_game()
                
            self._draw_game()
            time.sleep(0.05)  # ~20 FPS
            
    def _reset_game(self):
        self.dino_y = self.display.height - self.ground_height - self.dino_height
        self.dino_velocity = 0
        self.dino_on_ground = True
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0
        self.spawn_timer = 0
        self.speed = 2
        self.spawn_interval = 60
        
    def _jump(self):
        if self.dino_on_ground:
            self.dino_velocity = self.jump_power
            self.dino_on_ground = False
            
    def _update_game(self):
        self.frame_count += 1
        
        # Update dino physics
        if not self.dino_on_ground:
            self.dino_velocity += self.gravity
            self.dino_y += self.dino_velocity
            
            # Check ground collision
            ground_level = self.display.height - self.ground_height - self.dino_height
            if self.dino_y >= ground_level:
                self.dino_y = ground_level
                self.dino_velocity = 0
                self.dino_on_ground = True
                
        # Spawn obstacles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            obstacle_type = random.choice(['cactus', 'bird'])
            if obstacle_type == 'bird':
                # Bird flies at random height
                obstacle_y = random.randint(self.display.height - self.ground_height - 16, 
                                          self.display.height - self.ground_height - 8)
            else:
                # Cactus on ground
                obstacle_y = self.display.height - self.ground_height - self.obstacle_height
                
            self.obstacles.append({
                'x': self.display.width,
                'y': obstacle_y,
                'type': obstacle_type,
                'width': self.obstacle_width,
                'height': self.obstacle_height
            })
            self.spawn_timer = 0
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle['x'] -= self.speed
            
            # Remove off-screen obstacles
            if obstacle['x'] + obstacle['width'] < 0:
                self.obstacles.remove(obstacle)
                self.score += 1
                
        # Check collisions
        dino_rect = {
            'x': self.dino_x,
            'y': self.dino_y,
            'width': self.dino_width,
            'height': self.dino_height
        }
        
        for obstacle in self.obstacles:
            if self._check_collision(dino_rect, obstacle):
                self.game_over = True
                return
                
        # Increase difficulty
        if self.frame_count % 300 == 0:  # Every 15 seconds
            self.speed = min(self.speed + 0.5, 6)
            self.spawn_interval = max(self.spawn_interval - 2, 30)
            
    def _check_collision(self, rect1, rect2):
        return (rect1['x'] < rect2['x'] + rect2['width'] and
                rect1['x'] + rect1['width'] > rect2['x'] and
                rect1['y'] < rect2['y'] + rect2['height'] and
                rect1['y'] + rect1['height'] > rect2['y'])
                
    def _draw_game(self):
        try:
            image = Image.new("1", (self.display.width, self.display.height))
            draw = ImageDraw.Draw(image)
            
            if self.game_over:
                self.display.draw_centered_text(f"Game Over!\nScore: {self.score}\nPress SELECT")
                return
                
            # Draw ground
            ground_y = self.display.height - self.ground_height
            draw.line([(0, ground_y), (self.display.width, ground_y)], fill=255)
            
            # Draw dino (simple rectangle with animation)
            dino_char = '█' if self.dino_on_ground and (self.frame_count // 5) % 2 else '▮'
            draw.rectangle([self.dino_x, self.dino_y, 
                          self.dino_x + self.dino_width - 1, 
                          self.dino_y + self.dino_height - 1], fill=255)
            
            # Add simple "legs" animation when running
            if self.dino_on_ground:
                leg_offset = 1 if (self.frame_count // 3) % 2 else 0
                draw.rectangle([self.dino_x + leg_offset, 
                              self.dino_y + self.dino_height - 2,
                              self.dino_x + leg_offset + 1,
                              self.dino_y + self.dino_height - 1], fill=255)
                              
            # Draw obstacles
            for obstacle in self.obstacles:
                if obstacle['type'] == 'bird':
                    # Draw bird (smaller, animated)
                    bird_frame = (self.frame_count // 4) % 2
                    if bird_frame:
                        draw.rectangle([obstacle['x'], obstacle['y'], 
                                      obstacle['x'] + obstacle['width'] - 1, 
                                      obstacle['y'] + obstacle['height'] - 1], fill=255)
                else:
                    # Draw cactus
                    draw.rectangle([obstacle['x'], obstacle['y'], 
                                  obstacle['x'] + obstacle['width'] - 1, 
                                  obstacle['y'] + obstacle['height'] - 1], fill=255)
                    # Add spikes
                    draw.point((obstacle['x'], obstacle['y'] + 2), fill=255)
                    draw.point((obstacle['x'] + obstacle['width'] - 1, obstacle['y'] + 3), fill=255)
                    
            # Draw score
            draw.text((self.display.width - 30, 0), f"HI {self.score}", fill=255)
            
            self.display.oled.image(image)
            self.display.oled.show()
            
        except Exception as e:
            print(f"Dino game draw error: {e}")
            self.display.draw_centered_text(f"Draw error:\n{str(e)[:15]}")