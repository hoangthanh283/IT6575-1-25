#!/usr/bin/env python3
import socket
import sys
import threading
import time

try:
    from server.kvss_server import KVSSServer
except ModuleNotFoundError:
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from server.kvss_server import KVSSServer


def get_free_port() -> int:
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp.bind(("127.0.0.1", 0))
    port = tmp.getsockname()[1]
    tmp.close()
    return port


class KVSSTestClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 5050) -> None:
        self.host = host
        self.port = port

    def send_request(self, request: str) -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))

            sock.send((request + "\n").encode("utf-8"))
            response = sock.recv(1024).decode("utf-8").strip()

            sock.close()
            return response
        except Exception as e:
            return f"ERROR: {e}"


def run_test_case(
    test_num: int,
    description: str,
    request: str,
    expected: str,
    client: KVSSTestClient,
) -> bool:
    print(f"\n--- Test Case {test_num}: {description} ---")
    print(f"Request: {request}")

    response = client.send_request(request)
    print(f"Response: {response}")

    if expected in response or response.startswith(expected):
        print("Pass")
        return True
    else:
        print(f"Fail - Expected: {expected}")
        return False


def run_all_tests() -> bool:
    print("=" * 60)
    print("KVSS Test Suite - 10 Test Cases")
    print("=" * 60)

    port = get_free_port()
    server = KVSSServer(port=port)
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    client = KVSSTestClient(port=port)
    passed = 0
    total = 10
    try:
        if run_test_case(
            1,
            "Valid PUT operation (new key)",
            "KV/1.0 PUT user42 Alice",
            "201 CREATED",
            client,
        ):
            passed += 1

        if run_test_case(
            2,
            "Valid GET operation",
            "KV/1.0 GET user42",
            "200 OK Alice",
            client,
        ):
            passed += 1

        if run_test_case(
            3,
            "Valid PUT operation (existing key)",
            "KV/1.0 PUT user42 Bob",
            "200 OK",
            client,
        ):
            passed += 1

        if run_test_case(
            4,
            "Valid DEL operation",
            "KV/1.0 DEL user42",
            "204 NO_CONTENT",
            client,
        ):
            passed += 1

        if run_test_case(
            5,
            "Valid STATS operation",
            "KV/1.0 STATS",
            "200 OK keys=",
            client,
        ):
            passed += 1

        if run_test_case(
            6,
            "Error: Missing version",
            "PUT user43 Charlie",
            "400 BAD_REQUEST",
            client,
        ):
            passed += 1

        if run_test_case(
            7,
            "Error: Wrong version",
            "KV/2.0 GET user42",
            "426 UPGRADE_REQUIRED",
            client,
        ):
            passed += 1

        if run_test_case(
            8,
            "Error: Invalid command",
            "KV/1.0 POTT user42 Alice",
            "400 BAD_REQUEST",
            client,
        ):
            passed += 1

        if run_test_case(
            9,
            "Error: GET non-existent key",
            "KV/1.0 GET nonexistent",
            "404 NOT_FOUND",
            client,
        ):
            passed += 1

        if run_test_case(
            10,
            "Error: PUT without value",
            "KV/1.0 PUT user44",
            "400 BAD_REQUEST",
            client,
        ):
            passed += 1

    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        try:
            client.send_request("KV/1.0 QUIT")
        except Exception:
            pass
        server.stop()

    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    if passed != total:
        print(f"{total - passed} tests failed")
    return passed == total


def run_manual_test_sequence(port: int) -> None:
    print("\n" + "=" * 60)
    print("MANUAL TEST SEQUENCE (from lab examples)")
    print("=" * 60)

    client = KVSSTestClient(port=port)

    test_sequence = [
        ("KV/1.0 PUT user42 Alice", "201 CREATED"),
        ("KV/1.0 GET user42", "200 OK Alice"),
        ("KV/1.0 DEL user42", "204 NO_CONTENT"),
        ("KV/1.0 GET user42", "404 NOT_FOUND"),
        ("KV/1.0 STATS", "200 OK keys=0"),
        ("KV/1.0 QUIT", "200 OK bye"),
    ]

    for i, (request, expected) in enumerate(test_sequence, 1):
        print(f"\nStep {i}:")
        print(f"C: {request}")
        response = client.send_request(request)
        print(f"S: {response}")

        if expected in response:
            print("Match expected response")
        else:
            print(f"Expected: {expected}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        port = get_free_port()
        server = KVSSServer(port=port)
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()
        time.sleep(1)

        run_manual_test_sequence(port)

        server.stop()
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)
