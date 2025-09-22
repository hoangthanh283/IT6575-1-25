#!/bin/bash

echo "=========================================="
echo "KVSS Port Cleanup Script"
echo "=========================================="

echo "Checking for processes using port 5050..."

if lsof -i :5050 >/dev/null 2>&1; then
    echo "Port 5050 is in use. Details:"
    lsof -i :5050
    echo ""
    
    PIDS=$(lsof -t -i :5050 2>/dev/null)
    
    if [ ! -z "$PIDS" ]; then
        echo "Killing processes: $PIDS"
        for PID in $PIDS; do
            echo "Killing process $PID..."
            kill -9 $PID 2>/dev/null || true
        done
        sleep 1
    fi
else
    echo "Port 5050 is free."
fi

echo ""
echo "Checking for KVSS server processes..."
KVSS_PIDS=$(pgrep -f "python3.*kvss_server.py" 2>/dev/null || true)

if [ ! -z "$KVSS_PIDS" ]; then
    echo "Found KVSS server processes: $KVSS_PIDS"
    pkill -f "python3.*kvss_server.py" 2>/dev/null || true
    sleep 1
    echo "KVSS server processes terminated."
else
    echo "No KVSS server processes found."
fi

echo ""
echo "Final check..."
if lsof -i :5050 >/dev/null 2>&1; then
    echo "Port 5050 is still in use. Manual intervention may be required."
    lsof -i :5050
else
    echo "Port 5050 is now free."
fi

if pgrep -f "python3.*kvss_server.py" >/dev/null 2>&1; then
    echo "KVSS server processes are still running."
    pgrep -f "python3.*kvss_server.py"
else
    echo "No KVSS server processes running."
fi