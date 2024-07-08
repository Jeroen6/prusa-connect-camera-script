#!/bin/bash

# Define the Python file that was set to run on boot
PYTHON_FILE="/path/to/your_script.py"

# Find the process ID (PID) of the running Python script
PID=$(pgrep -f "$PYTHON_FILE")

if [ -z "$PID" ]; then
    echo "No process found running for $PYTHON_FILE."
else
    # Kill the process
    kill $PID
    echo "Process $PID running $PYTHON_FILE has been killed."
fi