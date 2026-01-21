import requests
import json

# Create a test user for the application
BASE_URL = "http://127.0.0.1:8000"

def create_test_user():
    """Create a test user account"""
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register",
                                json=user_data,
                                headers={"Content-Type": "application/json"})

        if response.status_code == 201:
            print("[OK] Test user created successfully!")
            print(f"Email: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            return True
        elif response.status_code == 400:
            print("[INFO] Test user already exists (this is OK)")
            return True
        else:
            print(f"[ERROR] Failed to create test user: {response.status_code}")
            error_data = response.json() if response.content else {}
            print(f"Error: {error_data}")
            return False
    except Exception as e:
        print(f"[ERROR] Error creating test user: {e}")
        return False

if __name__ == "__main__":
    print("Creating test user account...")
    create_test_user()
    print("\nYou can now use these credentials to log in:")
    print("- Email: test@example.com")
    print("- Password: password123")