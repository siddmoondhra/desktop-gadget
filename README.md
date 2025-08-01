# Raspberry Pi OLED Multi-App Device

A handheld device with OLED display and tactile buttons running multiple apps including weather, notes, Spotify control, timer, and classic games like Snake and Dino Runner.

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
   git clone https://github.com/siddmoondhra/desktop-gadget.git
   cd desktop-gadget
   ```

2. Run setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Configure API keys:
   ```bash
   cp .env.template .env
   nano .env
   ```

4. Run the project:
   ```bash
   ./scripts/run.sh
   ```

## Optional: Auto-start on boot

```bash
./scripts/install_service.sh
sudo systemctl start oled-device
```

## Apps & Games

### Apps
- **Weather**: Current conditions with OpenWeatherMap API (scrollable display, auto-refresh)
- **Sweet Notes**: Cycling through custom messages and encouragement
- **Spotify**: Music control (play/pause/next/previous) with track display
- **Timer**: Countdown timer with presets (1, 5, 10, 30, 60 minutes)

### Games
- **Snake**: Classic snake game 
- **Dino Runner**: Chrome-inspired side-scrolling obstacle avoidance game

## Game Controls

### Snake Game
- **Up/Down/Select/Back**: Move in absolute directions (up=up, select=right, back=left)
- **Double-tap Back**: Exit game
- Snake cannot reverse into itself 

### Dino Runner
- **Select**: Jump
- **Down**: Fast-fall (while jumping)
- **Up**: Turbo boost
- **Back**: Exit game

## Service Management

Once installed as a service, control it with:

```bash
# Start/stop/restart
sudo systemctl {start|stop|restart} oled-device

# Check status
sudo systemctl status oled-device

# View live logs
journalctl -u oled-device -f
```

## Development

### Making Changes
```bash
# Stop service for development
sudo systemctl stop oled-device

# Run manually for testing
./scripts/run.sh

# Restart service when done
sudo systemctl start oled-device
```

### Adding New Apps
1. Create app file in `apps/` directory with `run()` method
2. Add import to `apps/__init__.py`
3. Add to app list in `main.py`
4. Restart service

## API Keys Required

- OpenWeatherMap API key for weather
- Spotify app credentials for music control

See `.env.template` for configuration details.

## Troubleshooting

### Common Issues
- **Display not working**: Check I2C is enabled (`sudo raspi-config`)
- **Service won't start**: Check logs with `journalctl -u oled-device -n 50`
- **Virtual environment issues**: Re-run `./setup.sh`
- **Git corruption**: Backup files, fresh clone, restore `venv/` and `.env`

### Hardware Test
```bash
# Check I2C connection
sudo i2cdetect -y 1  # Should show 0x3C

# Test manual run first
source venv/bin/activate
python main.py
```