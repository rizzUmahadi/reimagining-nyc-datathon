import requests
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
params = {
    "email": EMAIL, "key": KEY,
    "param": "88101",
    "state": "36", "county": "005",
    "bdate": "20260801", "edate": "20260831",
}

resp = requests.get(url, params=params)
data = resp.json()

df = pd.DataFrame(data.get('Data', []))
print(f"Rows returned: {len(df)}")
if not df.empty:
    print(df[['site_number', 'local_site_name', 'date_local', 'arithmetic_mean', 'units_of_measure']].to_string(index=False))