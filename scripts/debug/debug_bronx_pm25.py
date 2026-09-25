import requests

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

for label, bdate, edate in [
    ("Aug 2026", "20260801", "20260831"),
    ("Jan 2026", "20260101", "20260131"),
    ("Jul 2025", "20250701", "20250731"),
]:
    params = {
        "email": EMAIL, "key": KEY,
        "param": "88101",
        "state": "36", "county": "005",
        "bdate": bdate, "edate": edate,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    header = data.get('Header', [{}])[0]
    print(f"{label}: status={header.get('status')}, rows={len(data.get('Data', []))}")
    if header.get('status') != 'Success':
        print("  Full header:", header)