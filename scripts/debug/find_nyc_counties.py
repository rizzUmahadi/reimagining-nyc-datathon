import requests

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

# First, find county codes within New York State
url = "https://aqs.epa.gov/data/api/list/countiesByState"
params = {"email": EMAIL, "key": KEY, "state": "36"}

resp = requests.get(url, params=params)
data = resp.json()

# Filter to just NYC counties (Bronx, New York=Manhattan, Kings=Brooklyn, Queens, Richmond=Staten Island)
nyc_counties = ['Bronx', 'New York', 'Kings', 'Queens', 'Richmond']
for row in data['Data']:
    if row['value_represented'] in nyc_counties:
        print(row)