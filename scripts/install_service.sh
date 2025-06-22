#!/bin/bash

# Install systemd service for auto-start on boot

SERVICE_NAME="oled-device"
PROJECT_DIR=$(pwd)
USER=$(whoami)

# Create systemd service file
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=OLED Device Controller
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${PROJECT_DIR}
ExecStart=${PROJECT_DIR}/run.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service

echo "Service installed! Commands:"
echo "  Start: sudo systemctl start ${SERVICE_NAME}"
echo "  Stop:  sudo systemctl stop ${SERVICE_NAME}"
echo "  Status: sudo systemctl status ${SERVICE_NAME}"
echo "  Logs: journalctl -u ${SERVICE_NAME} -f"