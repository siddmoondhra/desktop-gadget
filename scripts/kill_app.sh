#!/bin/bash

echo "Stopping OLED Device..."

# Stop the systemd service
sudo systemctl stop oled-device

# Wait a moment
sleep 2

# Kill any remaining Python processes related to the project
PROJECT_DIR=$(pwd)
sudo pkill -f "$PROJECT_DIR/main.py"
sudo pkill -f "main.py"

# Kill any processes using the display
sudo pkill -f "ssd1306"
sudo pkill -f "oled"

# Check if anything is still running
REMAINING=$(ps aux | grep -E "(main\.py|ssd1306|oled)" | grep -v grep)
if [ ! -z "$REMAINING" ]; then
    echo "Warning: Some processes might still be running:"
    echo "$REMAINING"
    echo "You may need to reboot or use 'sudo pkill -9 python3'"
else
    echo "✅ All processes stopped successfully"
fi

# Clear the display
python3 -c "
try:
    import board, busio
    from lib.display import Display
    i2c = busio.I2C(board.SCL, board.SDA)
    display = Display(i2c, 128, 32, 0x3C)
    display.clear()
    print('Display cleared')
except: pass
"

echo "Safe to run manually now!"