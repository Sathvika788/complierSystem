#!/usr/bin/env python3
"""
Test script for API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("🧪 Testing health endpoint...")
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_languages():
    """Test languages endpoint"""
    print("\n🧪 Testing languages endpoint...")
    response = requests.get(f"{BASE_URL}/languages")
    print(f"Status: {response.status_code}")
    languages = response.json()
    print(f"Found {len(languages)} languages:")
    for lang in languages:
        print(f"  - {lang['name']} (ID: {lang['id']})")
    return response.status_code == 200

def test_python_submission():
    """Test Python code submission"""
    print("\n🧪 Testing Python submission...")
    submission_data = {
        "source_code": "print('Hello from Python!')\nfor i in range(3):\n    print(f'Count: {i}')",
        "language_id": 3,
        "stdin": "",
        "cpu_time_limit": 5.0
    }
    
    response = requests.post(f"{BASE_URL}/submissions", json=submission_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Submission ID: {result['submission_id']}")
    
    # Wait for completion
    submission_id = result['submission_id']
    for i in range(10):
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/submissions/{submission_id}")
        data = response.json()
        if data['status'] == 'Completed':
            print("✅ Python execution completed!")
            print(f"Output: {data['stdout']}")
            return True
        elif data['status'] == 'Error':
            print(f"❌ Python execution failed: {data['stderr']}")
            return False
    
    print("❌ Python execution timed out")
    return False

def test_sql_submission():
    """Test SQL code submission"""
    print("\n🧪 Testing SQL submission...")
    
    sql_code = """
    CREATE TABLE users (id INTEGER, name TEXT, age INTEGER);
    INSERT INTO users VALUES (1, 'Alice', 25), (2, 'Bob', 30), (3, 'Charlie', 35);
    SELECT * FROM users WHERE age > 28;
    """
    
    submission_data = {
        "source_code": sql_code,
        "language_id": 8,
        "stdin": "",
        "cpu_time_limit": 5.0
    }
    
    response = requests.post(f"{BASE_URL}/submissions", json=submission_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Submission ID: {result['submission_id']}")
    
    # Wait for completion
    submission_id = result['submission_id']
    for i in range(10):
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/submissions/{submission_id}")
        data = response.json()
        if data['status'] == 'Completed':
            print("✅ SQL execution completed!")
            print(f"Output: {data['stdout']}")
            return True
        elif data['status'] == 'Error':
            print(f"❌ SQL execution failed: {data['stderr']}")
            return False
    
    print("❌ SQL execution timed out")
    return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    
    tests = [
        test_health,
        test_languages,
        test_python_submission,
        test_sql_submission
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")

if __name__ == "__main__":
    main()