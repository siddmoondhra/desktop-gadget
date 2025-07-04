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
        
        # Scrolling variables
        self.scroll_position = 0
        self.weather_lines = []
        
    def run(self):
        # Initial weather fetch
        if not self.current_weather or self.current_weather == "Loading...":
            self._fetch_weather()
            
        while True:
            current_time = time.time()
            
            # Auto-refresh weather data
            if current_time - self.last_update > self.refresh_interval:
                self._fetch_weather()
                
            self._display_scrollable_weather()
            
            button = self.buttons.get_pressed()
            if button == 'back':
                return
            elif button == 'select':
                # Manual refresh
                self.current_weather = "Refreshing..."
                self.weather_lines = ["Refreshing..."]
                self.scroll_position = 0
                self.display.draw_centered_text(self.current_weather)
                self._fetch_weather()
            elif button == 'up':
                # Scroll up
                if self.scroll_position > 0:
                    self.scroll_position -= 1
                time.sleep(0.2)  # Prevent too fast scrolling
            elif button == 'down':
                # Scroll down
                max_scroll = max(0, len(self.weather_lines) - 2)  # Show 2 lines at a time
                if self.scroll_position < max_scroll:
                    self.scroll_position += 1
                time.sleep(0.2)  # Prevent too fast scrolling
                
            time.sleep(0.1)
    
    def _display_scrollable_weather(self):
        if not self.weather_lines:
            self.display.draw_centered_text("No weather data")
            return
        
        # Show 2 lines at a time based on scroll position
        visible_lines = self.weather_lines[self.scroll_position:self.scroll_position + 2]
        
        # Add scroll indicators
        scroll_text = "\n".join(visible_lines)
        
        # Add scroll indicators if there's more content
        if self.scroll_position > 0:
            scroll_text = "↑ " + scroll_text
        if self.scroll_position < len(self.weather_lines) - 2:
            scroll_text = scroll_text + " ↓"
            
        self.display.draw_centered_text(scroll_text)
            
    def _fetch_weather(self):
        if not self.api_key:
            self.current_weather = "No API key\nset in .env"
            self.weather_lines = ["No API key", "set in .env"]
            return
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'imperial'  # Fahrenheit
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                
                # Create scrollable lines
                self.weather_lines = [
                    f"{self.city}",
                    f"Temperature: {temp:.0f}°F",
                    f"Feels like: {feels_like:.0f}°F",
                    f"Condition: {desc.title()}",
                    f"Humidity: {humidity}%",
                    f"Wind: {wind_speed:.1f} mph"
                ]
                
                # Also keep the old format for fallback
                self.current_weather = f"{self.city}\n{temp:.0f}°F (feels {feels_like:.0f}°F)\n{desc.title()}\n{humidity}% humid"
                
                self.last_update = time.time()
                self.retry_count = 0
                self.scroll_position = 0  # Reset scroll when new data arrives
                
            elif response.status_code == 401:
                self.current_weather = "Invalid API key"
                self.weather_lines = ["Invalid API key"]
            elif response.status_code == 404:
                self.current_weather = f"City '{self.city}'\nnot found"
                self.weather_lines = [f"City '{self.city}'", "not found"]
            else:
                self.current_weather = f"Weather error\n{response.status_code}"
                self.weather_lines = ["Weather error", f"Code: {response.status_code}"]
                
        except requests.exceptions.Timeout:
            self.current_weather = "Connection\ntimeout"
            self.weather_lines = ["Connection", "timeout"]
        except requests.exceptions.ConnectionError:
            self.current_weather = "No internet\nconnection"
            self.weather_lines = ["No internet", "connection"]
        except Exception as e:
            self.retry_count += 1
            if self.retry_count <= self.max_retries:
                self.current_weather = f"Retrying...\n({self.retry_count}/{self.max_retries})"
                self.weather_lines = ["Retrying...", f"({self.retry_count}/{self.max_retries})"]
                time.sleep(2)  # Wait before retry
                self._fetch_weather()
            else:
                self.current_weather = f"Weather error:\n{str(e)[:20]}"
                self.weather_lines = ["Weather error:", str(e)[:20]]
                print(f"Weather error: {e}")