#!/bin/bash

# Define the Python file and its directory
SCRIPT_DIR=$(pwd)
PYTHON_FILE="prusa-connect-camera-upload.py"

# Full path to Python interpreter
PYTHON_INTERPRETER="/usr/bin/python3"

# Check if the cron job already exists
crontab -l | grep -q "@reboot cd $SCRIPT_DIR && $PYTHON_INTERPRETER $PYTHON_FILE"
if [ $? -eq 0 ]; then
    echo "Cron job already exists."
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "@reboot cd $SCRIPT_DIR && $PYTHON_INTERPRETER $PYTHON_FILE") | crontab -
    echo "Cron job added."
fi
