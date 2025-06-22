import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self, display, buttons):
        self.name = "Weather"
        self.display = display
        self.buttons = buttons
        self.city = os.getenv("WEATHER_CITY", "New York")
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.refresh_interval = 600  # 10 minutes to reduce API calls
        self.last_update = 0
        self.current_weather = "Loading..."
        self.retry_count = 0
        self.max_retries = 3
        
    def run(self):
        # Initial weather fetch
        if not self.current_weather or self.current_weather == "Loading...":
            self._fetch_weather()
            
        while True:
            current_time = time.time()
            
            # Auto-refresh weather data
            if current_time - self.last_update > self.refresh_interval:
                self._fetch_weather()
                
            self.display.draw_centered_text(self.current_weather)
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'select':
                # Manual refresh
                self.current_weather = "Refreshing..."
                self.display.draw_centered_text(self.current_weather)
                self._fetch_weather()
            elif button == 'up' or button == 'down':
                # Could implement city cycling here
                pass
                
            time.sleep(0.1)
            
    def _fetch_weather(self):
        if not self.api_key:
            self.current_weather = "No API key\nset in .env"
            return
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                
                self.current_weather = f"{self.city}\n{temp:.1f}°C ({feels_like:.0f}°C)\n{desc.title()}\n{humidity}% humidity"
                self.last_update = time.time()
                self.retry_count = 0
                
            elif response.status_code == 401:
                self.current_weather = "Invalid API key"
            elif response.status_code == 404:
                self.current_weather = f"City '{self.city}'\nnot found"
            else:
                self.current_weather = f"Weather error\n{response.status_code}"
                
        except requests.exceptions.Timeout:
            self.current_weather = "Connection\ntimeout"
        except requests.exceptions.ConnectionError:
            self.current_weather = "No internet\nconnection"
        except Exception as e:
            self.retry_count += 1
            if self.retry_count <= self.max_retries:
                self.current_weather = f"Retrying...\n({self.retry_count}/{self.max_retries})"
                time.sleep(2)  # Wait before retry
                self._fetch_weather()
            else:
                self.current_weather = f"Weather error:\n{str(e)[:20]}"
                print(f"Weather error: {e}")