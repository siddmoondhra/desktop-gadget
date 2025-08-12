#!/bin/bash

# Install systemd service for auto-start on boot

SERVICE_NAME="oled-device"
PROJECT_DIR=$(pwd)
USER=$(whoami)

echo "Installing OLED Device service..."
echo "Project directory: $PROJECT_DIR"
echo "User: $USER"

# Make sure run.sh is executable
chmod +x scripts/run.sh

# Create systemd service file
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=OLED Device Controller
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${PROJECT_DIR}
ExecStart=/bin/bash ${PROJECT_DIR}/scripts/run.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=HOME=/home/${USER}
Environment=PATH=/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service

echo ""
echo "✅ Service installed successfully!"
echo ""
echo "Commands to manage the service:"
echo "  Start:    sudo systemctl start ${SERVICE_NAME}"
echo "  Stop:     sudo systemctl stop ${SERVICE_NAME}"
echo "  Restart:  sudo systemctl restart ${SERVICE_NAME}"
echo "  Status:   sudo systemctl status ${SERVICE_NAME}"
echo "  Logs:     journalctl -u ${SERVICE_NAME} -f"
echo "  Disable:  sudo systemctl disable ${SERVICE_NAME}"
echo ""
echo "The service will now start automatically on boot."
echo "To start it now, run: sudo systemctl start ${SERVICE_NAME}"