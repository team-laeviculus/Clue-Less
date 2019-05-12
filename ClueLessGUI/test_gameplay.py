"""
Use this to add other players so you dont need multiple GUIs open
"""
import requests

NUM_FAKE_PLAYERS = 3


def add_player(name):
    print("DEBUG MODE ENABLED")
    url = "http://127.0.0.1:5000/games/players"
    r = requests.post(url, json={'name': f'{name}'})
    print(f"response: {r.json()}")
    return r


print(f"Creating {NUM_FAKE_PLAYERS} Fake Players")
for i in range(NUM_FAKE_PLAYERS):
    add_player(f"player_{i}")
