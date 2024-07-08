#!/bin/bash

# Define the Python file that was set to run on boot
PYTHON_FILE="./prusa-connect-camera-upload.py"

# Check if the cron job exists and remove it
crontab -l | grep -v "@reboot /usr/bin/python3 $PYTHON_FILE" | crontab -
echo "Cron job removed if it existed."
