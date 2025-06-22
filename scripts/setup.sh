#!/bin/bash

echo "Setting up Raspberry Pi OLED Project..."

# Update system
sudo apt update
sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv i2c-tools

# Enable I2C
sudo raspi-config nonint do_i2c 0

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python packages
pip install -r requirements.txt

# Copy environment template
if [ ! -f .env ]; then
    cp .env.template .env
    echo "Please edit .env file with your API keys"
fi

# Test I2C connection
echo "Testing I2C connection..."
i2cdetect -y 1

# Make the script executable
chmod +x scripts/run.sh

echo "Setup complete! Please:"
echo "1. Edit .env with your API keys"
echo "2. Run: ./scripts/run.sh"