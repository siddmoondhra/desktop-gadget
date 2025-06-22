from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class Display:
    def __init__(self, i2c, width=128, height=32, address=0x3C):
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=address)
        self.width = width
        self.height = height
        self.font = ImageFont.load_default()
        
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
        
    def draw_text(self, text, x=0, y=0):
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.text((x, y), text, font=self.font, fill=255)
        self.oled.image(image)
        self.oled.show()
        
    def draw_centered_text(self, text):
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        
        # Calculate text size and position
        text_width = draw.textlength(text, font=self.font)
        text_height = self.font.getsize(text)[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        draw.text((x, y), text, font=self.font, fill=255)
        self.oled.image(image)
        self.oled.show()