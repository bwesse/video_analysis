import requests

r = requests.post(
    "https://vbs.videobrowsing.org/api/v2/login",
    json={"username": "ivadl12", "password": "dcyaeAI5cflKtsg"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")

session_token = r.json()["sessionId"]

r = requests.get(
    f"https://vbs.videobrowsing.org/api/v2/client/evaluation/list?session={session_token}",
    headers={"Accept": "application/json"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")

# TODO: Use filter instead of picking first to ensure correct one is used
evaluation_id = r.json()[0]["id"]

data = {
    "answerSets": [
        {
            "answers": [
                {
                    "mediaItemName": "00001",
                    "start": 74570,
                    "end": 74570
                }
            ]
        }
    ]
}

r = requests.post(
    f"https://vbs.videobrowsing.org/api/v2/submit/{evaluation_id}?session={session_token}",
    json=data,
    headers={"Accept": "application/json"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")