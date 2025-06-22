# Raspberry Pi OLED Multi-App Device

A handheld device with OLED display and tactile buttons running multiple apps including weather, notes, Spotify control, and timer.

## Hardware

- Raspberry Pi Zero 2W
- 128x32 pixel 0.96" SSD1306 OLED display
- 4x Gikfun 3mm tactical button switches
- Jumper wires for connections

## Pin Configuration

- Button Up: GPIO 17
- Button Down: GPIO 27  
- Button Select: GPIO 22
- Button Back: GPIO 23
- OLED: I2C (SDA/SCL)

## Quick Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pi-oled-device.git
   cd pi-oled-device
   ```

2. Run setup script:
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. Configure API keys:
   ```bash
   nano .env
   ```

4. Run the project:
   ```bash
   ./scripts/run.sh
   ```

## Optional: Auto-start on boot

```bash
./scripts/install-service.sh
sudo systemctl start oled-device
```

## Apps

- **Weather**: Current conditions with OpenWeatherMap API
- **Sweet Notes**: Cycling through custom messages
- **Spotify**: Music control (play/pause/next/previous)
- **Timer**: Countdown timer with presets

## API Keys Required

- OpenWeatherMap API key for weather
- Spotify app credentials for music control

See `.env.template` for configuration details.