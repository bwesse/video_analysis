import requests

# Login
r = requests.post(
    "https://vbs.videobrowsing.org/api/v2/login",
    json={"username": "ivadl12", "password": "dcyaeAI5cflKtsg"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")

session_token = r.json()["sessionId"]

# Get evaluation list
r = requests.get(
    f"https://vbs.videobrowsing.org/api/v2/client/evaluation/list?session={session_token}",
    headers={"Accept": "application/json"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")

# Find the correct evaluation ID
evaluation_id = None
for evaluation in r.json():
    if evaluation["name"] == "IVADL2024":
        evaluation_id = evaluation["id"]
        break

if evaluation_id is None:
    raise ValueError("Evaluation 'IVADL2024' not found")

# Prepare submit data
task_name = "IVADL-TEST01"
data = {
    "taskName": task_name,
    "answerSets": [
        {
            "answers": [
                {
                    "text": None,
                    "mediaItemName": "00019",
                    "mediaCollectionName": "IVADL",
                    "start": 74570,
                    "end": 74570
                }
            ]
        }
    ]
}

# Submit
r = requests.post(
    f"https://vbs.videobrowsing.org/api/v2/submit/{evaluation_id}?session={session_token}",
    json=data,
    headers={"Accept": "application/json"},
    timeout=1000,
)

print(f"Status Code: {r.status_code}, Content: {r.json()}")