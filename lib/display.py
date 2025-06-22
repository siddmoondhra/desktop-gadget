from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import textwrap

class Display:
    def __init__(self, i2c, width=128, height=32, address=0x3C):
        try:
            self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=address)
            self.width = width
            self.height = height
            
            # Try to load a better font, fall back to default
            try:
                self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
            except:
                self.font = ImageFont.load_default()
                
            self.clear()
            
        except Exception as e:
            print(f"Display initialization error: {e}")
            raise
        
    def clear(self):
        try:
            self.oled.fill(0)
            self.oled.show()
        except Exception as e:
            print(f"Display clear error: {e}")
        
    def draw_text(self, text, x=0, y=0):
        try:
            image = Image.new("1", (self.width, self.height))
            draw = ImageDraw.Draw(image)
            draw.text((x, y), text, font=self.font, fill=255)
            self.oled.image(image)
            self.oled.show()
        except Exception as e:
            print(f"Display draw error: {e}")
        
    def draw_centered_text(self, text):
        try:
            image = Image.new("1", (self.width, self.height))
            draw = ImageDraw.Draw(image)
            
            # Handle multi-line text
            lines = text.split('\n')
            if len(lines) == 1:
                # Wrap long single lines
                wrapped = textwrap.fill(text, width=20)
                lines = wrapped.split('\n')
            
            # Calculate total text height
            line_height = 12
            total_height = len(lines) * line_height
            start_y = max(0, (self.height - total_height) // 2)
            
            for i, line in enumerate(lines):
                if i * line_height + start_y >= self.height:
                    break  # Don't draw off-screen
                    
                # Get text width for centering
                bbox = draw.textbbox((0, 0), line, font=self.font)
                text_width = bbox[2] - bbox[0]
                x = max(0, (self.width - text_width) // 2)
                y = start_y + i * line_height
                
                draw.text((x, y), line, font=self.font, fill=255)
            
            self.oled.image(image)
            self.oled.show()
            
        except Exception as e:
            print(f"Display centered text error: {e}")
            # Fallback to simple text
            self.draw_text(str(text)[:20], 0, 0)