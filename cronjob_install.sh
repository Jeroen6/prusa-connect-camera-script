#!/bin/bash

# Define the Python file and its directory
SCRIPT_DIR=$(pwd)
PYTHON_FILE="prusa-connect-camera-upload.py"

# Full path to Python interpreter
PYTHON_INTERPRETER="/usr/bin/python3"

# Delay startup on reboot to give networking time to initialize.
CRON_COMMAND="@reboot /bin/bash -lc 'sleep 20; cd $SCRIPT_DIR && $PYTHON_INTERPRETER $PYTHON_FILE >/dev/null 2>&1'"

# Check if the cron job already exists
crontab -l 2>/dev/null | grep -Fq "$CRON_COMMAND"
if [ $? -eq 0 ]; then
    echo "Cron job already exists."
else
    # Replace any older uploader @reboot entries and add the current command.
    (crontab -l 2>/dev/null | grep -v "$PYTHON_FILE"; echo "$CRON_COMMAND") | crontab -
    echo "Cron job added."
fi
