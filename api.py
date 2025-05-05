import requests

BASE_URL = "https://dabomb-api.onrender.com"

def get_users():
    response = requests.get(f"{BASE_URL}/users")
    return response.json() if response.ok else None

def get_user(uid):
    response = requests.get(f"{BASE_URL}/users/{uid}")
    return response.json() if response.ok else None

def get_unopened_messages(uid):
    url = f"{BASE_URL}/messages/unopened?uid={uid}"
    response = requests.get(url)
    return response.json() if response.ok else []

def get_messages(uid):
    response = requests.get(f"{BASE_URL}/messages", params={"uid": uid})
    return response.json() if response.ok else []

def get_all_opened_messages():
    response = requests.get(f"{BASE_URL}/messages/all/opened")
    return response.json() if response.ok else []

def send_message(sender_id, receiver_id, message_type, message):
    payload = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message_type": message_type,
        "message": message
    }
    response = requests.post(f"{BASE_URL}/messages/send", json=payload)
    return response.json() if response.ok else None

def open_message(message_id):
    response = requests.post(f"{BASE_URL}/messages/open/{message_id}")
    return response.ok

def get_points(uid):
    response = requests.get(f"{BASE_URL}/points/{uid}")
    return response.json() if response.ok else {"game_points": 0, "trust_points": 0}
