import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

token = os.getenv("MY_TOKEN")
player_tag = os.getenv("TAG_GONZALO")

url = f"https://api.clashroyale.com/v1/players/{player_tag.replace('#', '%23')}/battlelog"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=3))
else:
    print(f"Error {response.status_code}: {response.text}")
