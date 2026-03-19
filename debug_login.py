import requests

BASE_URL = "http://127.0.0.1:8080/api"

def test_login():
    payload = {
        "username": "flemick66",
        "password": "flemick123",
        "device_id": "hw-vujkqs" # match the one in DB to avoid 403
    }
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Text: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
