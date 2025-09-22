#!/bin/bash

echo "=========================================="
echo "KVSS (Key-Value Store Service) Demo"
echo "=========================================="

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

cleanup_existing_servers() {
    echo "Checking for existing KVSS servers..."
    pkill -f "python3.*kvss_server.py" 2>/dev/null || true
    sleep 1
    
    if lsof -i :5050 >/dev/null 2>&1; then
        echo "Port 5050 is still in use. Attempting to free it..."
        PID=$(lsof -t -i :5050 2>/dev/null)
        if [ ! -z "$PID" ]; then
            kill -9 $PID 2>/dev/null || true
            sleep 1
        fi
    fi
}

cleanup_existing_servers

echo "Starting KVSS Server in background..."

cd server
python3 kvss_server.py &
SERVER_PID=$!
cd ..

sleep 2

if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Error: Server failed to start. Check for port conflicts."
    exit 1
fi

echo "Server started successfully with PID: $SERVER_PID"
echo ""

echo "Running test sequence..."
echo "----------------------------------------"

cd tests
python3 test_kvss.py --manual
cd ..

echo ""
echo "Running full test suite..."
echo "----------------------------------------"

cd tests
python3 test_kvss.py
cd ..

echo ""
echo "Demo completed. Stopping server..."

stop_server() {
    if [ ! -z "$SERVER_PID" ] && kill -0 $SERVER_PID 2>/dev/null; then
        echo "Stopping server with PID: $SERVER_PID"
        kill $SERVER_PID 2>/dev/null
        
        sleep 2
        
        if kill -0 $SERVER_PID 2>/dev/null; then
            echo "Force stopping server..."
            kill -9 $SERVER_PID 2>/dev/null
        fi
    fi
    pkill -f "python3.*kvss_server.py" 2>/dev/null || true
}

trap stop_server EXIT
stop_server
echo "Server stopped."
echo "=========================================="
