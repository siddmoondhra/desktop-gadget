#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Create a PID file to track the process
PID_FILE="/tmp/oled_device.pid"

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    if [ -f "$PID_FILE" ]; then
        rm -f "$PID_FILE"
    fi
    # Clear display on exit
    python3 -c "
try:
    import board, busio
    from lib.display import Display
    i2c = busio.I2C(board.SCL, board.SDA)
    display = Display(i2c, 128, 32, 0x3C)
    display.clear()
except: pass
" 2>/dev/null
    exit 0
}

# Trap signals for clean exit
trap cleanup INT TERM EXIT

# Function to run the app with auto-restart
run_app() {
    while true; do
        echo "Starting OLED project..."
        echo $$ > "$PID_FILE"
        
        python3 main.py
        
        exit_code=$?
        if [ $exit_code -eq 0 ]; then
            echo "App exited normally"
            break
        else
            echo "App crashed with exit code $exit_code. Restarting in 5 seconds..."
            sleep 5
        fi
    done
}

run_app