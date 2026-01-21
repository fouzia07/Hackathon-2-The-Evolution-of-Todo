import requests
import json

# Test if the backend is running and accessible
BASE_URL = "http://127.0.0.1:8000"

def test_backend_health():
    """Test if the backend is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("[OK] Backend is accessible")
            print(f"Health check response: {response.json()}")
            return True
        else:
            print(f"[ERROR] Backend health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Backend is not accessible: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    endpoints = [
        "/",
        "/docs",
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/tasks"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print(f"[OK] {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {endpoint}: {e}")

if __name__ == "__main__":
    print("Testing backend connectivity...")
    if test_backend_health():
        print("\nTesting API endpoints...")
        test_api_endpoints()
    else:
        print("\nPlease make sure the backend server is running on http://127.0.0.1:8000")