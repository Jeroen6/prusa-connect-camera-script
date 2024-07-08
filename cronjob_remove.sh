#!/bin/bash

# Define the Python file and its directory
SCRIPT_DIR=$(pwd)
PYTHON_FILE="prusa-connect-camera-upload.py"

# Full path to Python interpreter
PYTHON_INTERPRETER="/usr/bin/python3"

# Check if the cron job exists and remove it
crontab -l | grep -v "@reboot cd $SCRIPT_DIR && $PYTHON_INTERPRETER $PYTHON_FILE" | crontab -
echo "Cron job removed if it existed."
