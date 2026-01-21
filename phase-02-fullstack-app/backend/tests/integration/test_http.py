#!/usr/bin/env python
"""
Test script to register a user via HTTP request to the running server.
"""

import requests
import json

def test_register():
    """Test registration via HTTP request."""
    url = "http://localhost:8000/api/v1/auth/register"

    payload = {
        "email": "test_http@example.com",
        "password": "shortpass123",
        "first_name": "Test",
        "last_name": "HTTP"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Making registration request...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_register()