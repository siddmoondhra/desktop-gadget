import requests
import time
import os
from dotenv import load_dotenv
from lib.display import Display

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self, display, buttons):
        self.name = "Weather"
        self.display = display
        self.buttons = buttons
        self.city = os.getenv("WEATHER_CITY", "New York")  # Default to NY if not set
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.refresh_interval = 300  # 5 minutes
        self.last_update = 0
        self.current_weather = "Loading..."
        
    def run(self):
        while True:
            current_time = time.time()
            if current_time - self.last_update > self.refresh_interval:
                self.current_weather = self._get_weather()
                self.last_update = current_time
                
            self.display.draw_centered_text(self.current_weather)
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'up':
                # Could implement temperature unit toggle here
                pass
            elif button == 'down':
                # Could implement city selection here
                pass
                
            time.sleep(0.1)
            
    def _get_weather(self):
        if not self.api_key:
            return "No API key set"
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if response.status_code != 200:
                return "Weather error"
                
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"{self.city}\n{temp:.1f}°C\n{desc.capitalize()}"
        except Exception as e:
            return f"Weather error: {str(e)}"
        


