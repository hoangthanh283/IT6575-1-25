#!/usr/bin/env python3
import logging
import socket
import threading
import time
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kvss_server.log"),
        logging.StreamHandler()
    ]
)


class KVSSServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 5050) -> None:
        self.host = host
        self.port = port
        self.storage: Dict[str, str] = {}
        self.start_time = time.time()
        self.requests_served = 0
        self.running = False
        self.socket = None

    def start(self) -> None:
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

    def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        try:
            with client_socket:
                while True:
                    data = client_socket.recv(1024).decode("utf-8").strip()
                    if not data:
                        break

                    logging.info(f"Request from {address}: {data}")
                    response = self.process_request(data)
                    logging.info(f"Response to {address}: {response}")

                    client_socket.send((response + "\n").encode("utf-8"))

                    if response.startswith("200 OK bye"):
                        break

        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            logging.info(f"Connection closed for {address}")

    def process_request(self, request: str) -> str:
        self.requests_served += 1

        try:
            parts = request.strip().split()
            if len(parts) < 2:
                return "400 BAD_REQUEST"

            version = parts[0]
            command = parts[1]

            if not version.startswith("KV/"):
                return "400 BAD_REQUEST"

            if version != "KV/1.0":
                return "426 UPGRADE_REQUIRED"

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

    def handle_put(self, args: list[str]) -> str:
        if len(args) < 2:
            return "400 BAD_REQUEST"

        key = args[0]
        value = " ".join(args[1:])

        if " " in key:
            return "400 BAD_REQUEST"

        is_new = key not in self.storage
        self.storage[key] = value

        return "201 CREATED" if is_new else "200 OK"

    def handle_get(self, args: list[str]) -> str:
        if len(args) != 1:
            return "400 BAD_REQUEST"

        key = args[0]

        if key in self.storage:
            return f"200 OK {self.storage[key]}"
        else:
            return "404 NOT_FOUND"

    def handle_del(self, args: list[str]) -> str:
        if len(args) != 1:
            return "400 BAD_REQUEST"

        key = args[0]

        if key in self.storage:
            del self.storage[key]
            return "204 NO_CONTENT"
        else:
            return "404 NOT_FOUND"

    def handle_stats(self) -> str:
        uptime = int(time.time() - self.start_time)
        keys_count = len(self.storage)
        return f"200 OK keys={keys_count} uptime={uptime}s served={self.requests_served}"

    def handle_quit(self) -> str:
        return "200 OK bye"

    def stop(self) -> None:
        self.running = False
        if self.socket:
            self.socket.close()


def main() -> None:
    server = KVSSServer()

    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
        server.stop()


if __name__ == "__main__":
    main()
