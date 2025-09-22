#!/usr/bin/env python3
"""
Mini Key-Value Store Service (KVSS) - Server
Distributed Systems Lab - Chapter 1

Interface Specification:
- Connection: TCP host:port (default 127.0.0.1:5050)
- Message unit: text line ending with \n (LF)
- Encoding: UTF-8
- Version: all requests start with KV/1.0 prefix
- Commands: PUT, GET, DEL, STATS, QUIT

Author: Distributed Systems Lab
Date: 2025
"""

import socket
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kvss_server.log'),
        logging.StreamHandler()
    ]
)

class KVSSServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 5050):
        self.host = host
        self.port = port
        self.storage: Dict[str, str] = {}
        self.start_time = time.time()
        self.requests_served = 0
        self.running = False
        self.socket = None
        
    def start(self):
        """Start the KVSS server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logging.info(f"KVSS Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    logging.info(f"New connection from {address}")
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        logging.error(f"Socket error: {e}")
                        
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()
                
    def handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle individual client connection"""
        try:
            with client_socket:
                while True:
                    data = client_socket.recv(1024).decode('utf-8').strip()
                    if not data:
                        break
                        
                    logging.info(f"Request from {address}: {data}")
                    response = self.process_request(data)
                    logging.info(f"Response to {address}: {response}")
                    
                    client_socket.send((response + '\n').encode('utf-8'))
                    
                    # Close connection if QUIT command
                    if response.startswith('200 OK bye'):
                        break
                        
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            logging.info(f"Connection closed for {address}")
            
    def process_request(self, request: str) -> str:
        """Process a single request and return response"""
        self.requests_served += 1
        
        try:
            parts = request.strip().split()
            if len(parts) < 2:
                return "400 BAD_REQUEST"
                
            version = parts[0]
            command = parts[1]
            
            # Check version
            if version != "KV/1.0":
                return "426 UPGRADE_REQUIRED"
                
            # Process commands
            if command == "PUT":
                return self.handle_put(parts[2:])
            elif command == "GET":
                return self.handle_get(parts[2:])
            elif command == "DEL":
                return self.handle_del(parts[2:])
            elif command == "STATS":
                return self.handle_stats()
            elif command == "QUIT":
                return self.handle_quit()
            else:
                return "400 BAD_REQUEST"
                
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return "500 SERVER_ERROR"
            
    def handle_put(self, args: list) -> str:
        """Handle PUT command"""
        if len(args) < 2:
            return "400 BAD_REQUEST"
            
        key = args[0]
        value = ' '.join(args[1:])  # Join in case value has spaces
        
        if ' ' in key:  # Key cannot contain spaces
            return "400 BAD_REQUEST"
            
        is_new = key not in self.storage
        self.storage[key] = value
        
        return "201 CREATED" if is_new else "200 OK"
        
    def handle_get(self, args: list) -> str:
        """Handle GET command"""
        if len(args) != 1:
            return "400 BAD_REQUEST"
            
        key = args[0]
        
        if key in self.storage:
            return f"200 OK {self.storage[key]}"
        else:
            return "404 NOT_FOUND"
            
    def handle_del(self, args: list) -> str:
        """Handle DEL command"""
        if len(args) != 1:
            return "400 BAD_REQUEST"
            
        key = args[0]
        
        if key in self.storage:
            del self.storage[key]
            return "204 NO_CONTENT"
        else:
            return "404 NOT_FOUND"
            
    def handle_stats(self) -> str:
        """Handle STATS command"""
        uptime = int(time.time() - self.start_time)
        keys_count = len(self.storage)
        return f"200 OK keys={keys_count} uptime={uptime}s served={self.requests_served}"
        
    def handle_quit(self) -> str:
        """Handle QUIT command"""
        return "200 OK bye"
        
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.socket:
            self.socket.close()

def main():
    """Main function to run the server"""
    server = KVSSServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
        server.stop()

if __name__ == "__main__":
    main()




