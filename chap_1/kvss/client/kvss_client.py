#!/usr/bin/env python3

import logging
import socket
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class KVSSClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5050) -> None:
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logging.info(
                f"Connected to KVSS server at {self.host}:{self.port}"
            )
            return True
        except Exception as e:
            logging.error(f"Failed to connect to server: {e}")
            return False

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.connected = False
            logging.info("Disconnected from server")

    def send_request(self, command: str) -> str:
        if not self.connected:
            return "ERROR: Not connected to server"

        try:
            if command.strip().upper() in ["HELP", "EXIT"]:
                return self.handle_local_command(command.strip().upper())
            request = f"KV/1.0 {command.strip()}"
            self.socket.send((request + "\n").encode("utf-8"))
            logging.info(f"Sent: {request}")
            response = self.socket.recv(1024).decode("utf-8").strip()
            logging.info(f"Received: {response}")
            return response
        except Exception as e:
            logging.error(f"Error sending request: {e}")
            return f"ERROR: {e}"

    def handle_local_command(self, command: str) -> str:
        if command == "HELP":
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
        elif command == "EXIT":
            return "CLIENT_EXIT"
        else:
            return "Unknown local command"

    def interactive_mode(self) -> None:
        print("KVSS Client - Interactive Mode")
        print('Type "HELP" for commands, "EXIT" to quit')
        print("-" * 40)
        while True:
            try:
                command = input("kvss> ").strip()
                if not command:
                    continue

                if command.upper() == "EXIT":
                    if self.connected:
                        self.send_request("QUIT")
                    break

                response = self.send_request(command)

                if response == "CLIENT_EXIT":
                    break

                print(f"Response: {response}")
                if response.startswith("200 OK bye"):
                    self.disconnect()

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break
        self.disconnect()

    def batch_mode(self, commands: list[str]) -> None:
        print("KVSS Client - Batch Mode")
        print("-" * 40)

        for command in commands:
            print(f"Command: {command}")
            response = self.send_request(command)
            print(f"Response: {response}")
            print()

            if response.startswith("200 OK bye"):
                self.disconnect()
                break

        if self.connected:
            self.disconnect()


def main() -> None:
    host = "127.0.0.1"
    port = 5050

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    client = KVSSClient(host, port)
    if not client.connect():
        print("Failed to connect to server. Make sure the server is running.")
        sys.exit(1)

    if sys.stdin.isatty():
        client.interactive_mode()
    else:
        commands = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                commands.append(line)
        client.batch_mode(commands)


if __name__ == "__main__":
    main()
