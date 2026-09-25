import requests
import pandas as pd

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

url = "https://aqs.epa.gov/data/api/dailyData/byCounty"
params = {
    "email": EMAIL, "key": KEY,
    "param": "88101",
    "state": "36", "county": "005",
    "bdate": "20260101", "edate": "20260731",
}

resp = requests.get(url, params=params)
data = resp.json()
df = pd.DataFrame(data.get('Data', []))

df['arithmetic_mean'] = pd.to_numeric(df['arithmetic_mean'], errors='coerce')

print(f"Total readings: {len(df)}")
print(f"Distinct sites: {df['local_site_name'].nunique()}")
print(f"\nAverage PM2.5 by site, Jan-Jul 2026:")
print(df.groupby('local_site_name')['arithmetic_mean'].mean())

print(f"\nOverall Bronx average, Jan-Jul 2026: {df['arithmetic_mean'].mean():.2f}")

df.to_csv('data/bronx_pm25_epa_2026.csv', index=False)
print("\nSaved to data/bronx_pm25_epa_2026.csv")