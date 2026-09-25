import requests
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.environ["AQS_EMAIL"]
KEY = os.environ["AQS_KEY"]

url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

all_years = []
for year, bdate, edate in [
    (2024, "20240101", "20240731"),
    (2025, "20250101", "20250731"),
    (2026, "20260101", "20260731"),
]:
    params = {
        "email": EMAIL, "key": KEY,
        "param": "88101",
        "state": "36", "county": "005",
        "bdate": bdate, "edate": edate,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    df = pd.DataFrame(data.get('Data', []))
    if df.empty:
        print(f"{year}: NO DATA")
        continue
    df['arithmetic_mean'] = pd.to_numeric(df['arithmetic_mean'], errors='coerce')
    df['Year'] = year
    all_years.append(df)
    print(f"{year}: {len(df)} readings, {df['local_site_name'].nunique()} sites, avg = {df['arithmetic_mean'].mean():.2f}")

combined = pd.concat(all_years, ignore_index=True)
combined.to_csv('data/bronx_pm25_epa_2024_2025_2026.csv', index=False)
print("\nSaved combined file")

print("\nBy site, by year:")
print(combined.groupby(['local_site_name', 'Year'])['arithmetic_mean'].mean())