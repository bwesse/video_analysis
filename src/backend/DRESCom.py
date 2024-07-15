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

evaluation_id = None
for evaluation in r.json():
    if evaluation["name"] == "IVADL2024":
        evaluation_id = evaluation["id"]
        break

if evaluation_id is None:
    raise ValueError("Evaluation 'IVADL2024' not found")


task_name = "IVADL-TEST01"  #update with current task name

data = {
    
    "answerSets": [
        {
            "taskName": task_name,
            "answers": [
                {
                    "text": None,
                    "mediaItemName": "00189",   #update to fit found item
                    "mediaCollection": "IVADL",
                    "start": 74570, #timestamp of the found item
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
print(f"JSON data being sent: {data}")  #debugging reasons