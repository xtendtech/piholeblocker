#!/bin/bash
set -e

echo "Installing Pi-hole Blocker..."

# 1. Copy the script to /usr/local/bin and make it executable
sudo cp piholeblocker.py /usr/local/bin/piholeblocker.py
sudo chmod +x /usr/local/bin/piholeblocker.py

# 2. Copy the systemd service file to /etc/systemd/system/
sudo cp piholeblocker.service /etc/systemd/system/piholeblocker.service
sudo chmod 644 /etc/systemd/system/piholeblocker.service

# 3. Reload systemd, enable on boot, and start immediately
sudo systemctl daemon-reload
sudo systemctl enable --now piholeblocker.service

# Fetch the public IP address silently
IP_ADDRESS=$(curl -s ifconfig.me/ip)

# Construct the target URL
TARGET_URL="http://${IP_ADDRESS}:8080/secret-open-sesame"

# Output the result
echo "$TARGET_URL"

echo "Done! Service is installed and running."
