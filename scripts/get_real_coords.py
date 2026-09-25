import requests

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

url = "https://aqs.epa.gov/data/api/monitors/byCounty"
for county, name in [("005", "Bronx"), ("061", "Manhattan")]:
    params = {
        "email": EMAIL, "key": KEY, "param": "88101",
        "state": "36", "county": county,
        "bdate": "20240101", "edate": "20261231",
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    seen = set()
    for row in data.get('Data', []):
        site = row.get('local_site_name')
        lat = row.get('latitude')
        lon = row.get('longitude')
        if site not in seen:
            seen.add(site)
            print(f"{name}: {site} -> lat={lat}, lon={lon}")