#!/bin/bash

# Define the Python file that was set to run on boot
PYTHON_FILE="prusa-connect-camera-upload.py"

# Remove any @reboot entry that launches the uploader script
crontab -l 2>/dev/null | grep -v "$PYTHON_FILE" | crontab -
echo "Cron job removed if it existed."
