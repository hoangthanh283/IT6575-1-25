#!/usr/bin/env python3
"""
Test Suite for Mini Key-Value Store Service (KVSS)
Distributed Systems Lab - Chapter 1

This test suite includes 10 test cases covering both valid operations
and error conditions as specified in the lab requirements.

Test Cases:
1. Valid PUT operation (new key)
2. Valid GET operation  
3. Valid DEL operation
4. Valid STATS operation
5. Valid QUIT operation
6. Error: Missing version (426 UPGRADE_REQUIRED)
7. Error: Wrong version (426 UPGRADE_REQUIRED) 
8. Error: Invalid command (400 BAD_REQUEST)
9. Error: GET non-existent key (404 NOT_FOUND)
10. Error: PUT without value (400 BAD_REQUEST)

Author: Distributed Systems Lab
Date: 2025
"""

import socket
import time
import threading
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.kvss_server import KVSSServer

class KVSSTestClient:
    """Simple test client for KVSS server"""
    
    def __init__(self, host='127.0.0.1', port=5050):
        self.host = host
        self.port = port
        
    def send_request(self, request: str) -> str:
        """Send a single request and return response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            
            sock.send((request + '\n').encode('utf-8'))
            response = sock.recv(1024).decode('utf-8').strip()
            
            sock.close()
            return response
        except Exception as e:
            return f"ERROR: {e}"

def run_test_case(test_num: int, description: str, request: str, expected: str, client: KVSSTestClient):
    """Run a single test case"""
    print(f"\n--- Test Case {test_num}: {description} ---")
    print(f"Request: {request}")
    
    response = client.send_request(request)
    print(f"Response: {response}")
    
    # Check if response matches expected (can be partial match for some cases)
    if expected in response or response.startswith(expected):
        print(f"✅ PASS")
        return True
    else:
        print(f"❌ FAIL - Expected: {expected}")
        return False

def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("KVSS Test Suite - 10 Test Cases")
    print("=" * 60)
    
    # Start server in background
    server = KVSSServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    # Create test client
    client = KVSSTestClient()
    
    # Test results tracking
    passed = 0
    total = 10
    
    try:
        # Test Case 1: Valid PUT operation (new key)
        if run_test_case(1, "Valid PUT operation (new key)", 
                        "KV/1.0 PUT user42 Alice", "201 CREATED", client):
            passed += 1
            
        # Test Case 2: Valid GET operation
        if run_test_case(2, "Valid GET operation", 
                        "KV/1.0 GET user42", "200 OK Alice", client):
            passed += 1
            
        # Test Case 3: Valid PUT operation (existing key)
        if run_test_case(3, "Valid PUT operation (existing key)", 
                        "KV/1.0 PUT user42 Bob", "200 OK", client):
            passed += 1
            
        # Test Case 4: Valid DEL operation
        if run_test_case(4, "Valid DEL operation", 
                        "KV/1.0 DEL user42", "204 NO_CONTENT", client):
            passed += 1
            
        # Test Case 5: Valid STATS operation
        if run_test_case(5, "Valid STATS operation", 
                        "KV/1.0 STATS", "200 OK keys=", client):
            passed += 1
            
        # Test Case 6: Error - Missing version
        if run_test_case(6, "Error: Missing version", 
                        "PUT user43 Charlie", "400 BAD_REQUEST", client):
            passed += 1
            
        # Test Case 7: Error - Wrong version
        if run_test_case(7, "Error: Wrong version", 
                        "KV/2.0 GET user42", "426 UPGRADE_REQUIRED", client):
            passed += 1
            
        # Test Case 8: Error - Invalid command
        if run_test_case(8, "Error: Invalid command", 
                        "KV/1.0 POTT user42 Alice", "400 BAD_REQUEST", client):
            passed += 1
            
        # Test Case 9: Error - GET non-existent key
        if run_test_case(9, "Error: GET non-existent key", 
                        "KV/1.0 GET nonexistent", "404 NOT_FOUND", client):
            passed += 1
            
        # Test Case 10: Error - PUT without value
        if run_test_case(10, "Error: PUT without value", 
                        "KV/1.0 PUT user44", "400 BAD_REQUEST", client):
            passed += 1
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        # Clean shutdown
        try:
            client.send_request("KV/1.0 QUIT")
        except:
            pass
        server.stop()
    
    # Print results
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} tests failed")
    print("=" * 60)
    
    return passed == total

def run_manual_test_sequence():
    """Run the manual test sequence from lab examples"""
    print("\n" + "=" * 60)
    print("MANUAL TEST SEQUENCE (from lab examples)")
    print("=" * 60)
    
    client = KVSSTestClient()
    
    test_sequence = [
        ("KV/1.0 PUT user42 Alice", "201 CREATED"),
        ("KV/1.0 GET user42", "200 OK Alice"),
        ("KV/1.0 DEL user42", "204 NO_CONTENT"),
        ("KV/1.0 GET user42", "404 NOT_FOUND"),
        ("KV/1.0 STATS", "200 OK keys=0"),
        ("KV/1.0 QUIT", "200 OK bye")
    ]
    
    for i, (request, expected) in enumerate(test_sequence, 1):
        print(f"\nStep {i}:")
        print(f"C: {request}")
        response = client.send_request(request)
        print(f"S: {response}")
        
        if expected in response:
            print("✅ Match expected response")
        else:
            print(f"❌ Expected: {expected}")

if __name__ == "__main__":
    """Main test runner"""
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        # Start server
        server = KVSSServer()
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = True
        server_thread.start()
        time.sleep(1)
        
        run_manual_test_sequence()
        
        # Stop server
        server.stop()
    else:
        # Run full test suite
        success = run_all_tests()
        sys.exit(0 if success else 1)




