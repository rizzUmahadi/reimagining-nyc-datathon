import requests

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

url = "https://aqs.epa.gov/data/api/list/states"
params = {"email": EMAIL, "key": KEY}

resp = requests.get(url, params=params)
print("Status:", resp.status_code)
print(resp.json())