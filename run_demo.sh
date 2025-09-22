#!/bin/bash

# Demo script for KVSS (Key-Value Store Service)
# This script demonstrates the basic functionality of the KVSS system

echo "=========================================="
echo "KVSS (Key-Value Store Service) Demo"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Starting KVSS Server in background..."

# Start server in background
cd server
python3 kvss_server.py &
SERVER_PID=$!
cd ..

# Wait for server to start
sleep 2

echo "Server started with PID: $SERVER_PID"
echo ""

echo "Running test sequence..."
echo "----------------------------------------"

# Run the test sequence
cd tests
python3 test_kvss.py --manual
cd ..

echo ""
echo "Running full test suite..."
echo "----------------------------------------"

# Run full test suite
cd tests
python3 test_kvss.py
cd ..

echo ""
echo "Demo completed. Stopping server..."

# Kill the server
kill $SERVER_PID 2>/dev/null

echo "Server stopped."
echo "=========================================="




