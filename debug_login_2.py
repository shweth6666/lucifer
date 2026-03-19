import requests

BASE_URL = "http://127.0.0.1:8080/api"

def test_login_wrong_device():
    payload = {
        "username": "flemick66",
        "password": "flemick123",
        "device_id": "something_else" 
    }
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login_wrong_device()
