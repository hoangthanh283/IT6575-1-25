#!/usr/bin/env python3
"""
Mini Key-Value Store Service (KVSS) - Client
Distributed Systems Lab - Chapter 1

Command line client that reads from stdin and sends requests to KVSS server
following the KV/1.0 protocol specification.

Usage:
    python3 kvss_client.py [host] [port]
    
Commands:
    PUT key value - Store key-value pair
    GET key      - Retrieve value for key
    DEL key      - Delete key
    STATS        - Get server statistics
    QUIT         - Disconnect from server
    HELP         - Show this help message
    EXIT         - Exit client

Author: Distributed Systems Lab
Date: 2025
"""

import socket
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class KVSSClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 5050):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
    def connect(self) -> bool:
        """Connect to KVSS server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logging.info(f"Connected to KVSS server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to server: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            self.socket.close()
            self.connected = False
            logging.info("Disconnected from server")
            
    def send_request(self, command: str) -> str:
        """Send request to server and return response"""
        if not self.connected:
            return "ERROR: Not connected to server"
            
        try:
            # Format request with KV/1.0 protocol
            if command.strip().upper() in ['HELP', 'EXIT']:
                return self.handle_local_command(command.strip().upper())
                
            request = f"KV/1.0 {command.strip()}"
            
            # Send request
            self.socket.send((request + '\n').encode('utf-8'))
            logging.info(f"Sent: {request}")
            
            # Receive response
            response = self.socket.recv(1024).decode('utf-8').strip()
            logging.info(f"Received: {response}")
            
            return response
            
        except Exception as e:
            logging.error(f"Error sending request: {e}")
            return f"ERROR: {e}"
            
    def handle_local_command(self, command: str) -> str:
        """Handle local client commands"""
        if command == 'HELP':
            return """
Available commands:
  PUT key value - Store key-value pair
  GET key      - Retrieve value for key  
  DEL key      - Delete key
  STATS        - Get server statistics
  QUIT         - Disconnect from server
  HELP         - Show this help message
  EXIT         - Exit client

Examples:
  PUT user42 Alice
  GET user42
  DEL user42
  STATS
"""
        elif command == 'EXIT':
            return "CLIENT_EXIT"
        else:
            return "Unknown local command"
            
    def interactive_mode(self):
        """Run client in interactive mode"""
        print("KVSS Client - Interactive Mode")
        print("Type 'HELP' for commands, 'EXIT' to quit")
        print("-" * 40)
        
        while True:
            try:
                command = input("kvss> ").strip()
                
                if not command:
                    continue
                    
                if command.upper() == 'EXIT':
                    if self.connected:
                        # Send QUIT to server before exiting
                        self.send_request("QUIT")
                    break
                    
                response = self.send_request(command)
                
                if response == "CLIENT_EXIT":
                    break
                    
                print(f"Response: {response}")
                
                # If server says bye, disconnect
                if response.startswith('200 OK bye'):
                    self.disconnect()
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break
                
        self.disconnect()
        
    def batch_mode(self, commands: list):
        """Run client in batch mode with predefined commands"""
        print("KVSS Client - Batch Mode")
        print("-" * 40)
        
        for command in commands:
            print(f"Command: {command}")
            response = self.send_request(command)
            print(f"Response: {response}")
            print()
            
            # If server says bye, disconnect
            if response.startswith('200 OK bye'):
                self.disconnect()
                break
                
        if self.connected:
            self.disconnect()

def main():
    """Main function"""
    # Parse command line arguments
    host = '127.0.0.1'
    port = 5050
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        
    # Create client
    client = KVSSClient(host, port)
    
    # Connect to server
    if not client.connect():
        print("Failed to connect to server. Make sure the server is running.")
        sys.exit(1)
        
    # Check if running in interactive mode or with stdin
    if sys.stdin.isatty():
        # Interactive mode
        client.interactive_mode()
    else:
        # Batch mode - read commands from stdin
        commands = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                commands.append(line)
        client.batch_mode(commands)

if __name__ == "__main__":
    main()




