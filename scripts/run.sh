#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Function to run the app with auto-restart
run_app() {
    while true; do
        echo "Starting OLED project..."
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

# Trap Ctrl+C to clean exit
trap 'echo "Shutting down..."; exit 0' INT

run_app