import requests
import pandas as pd

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

# Get Bronx sensors from a recent day
resp = requests.get(URL, params={
    "$select": "distinct link_id, link_name",
    "$where": "borough = 'Bronx' AND data_as_of between '2026-09-01T00:00:00' and '2026-09-01T23:59:59'",
    "$limit": 50,
})
df = pd.DataFrame(resp.json())
print(f"Bronx sensors found (recent): {len(df)}")
print(df.to_string(index=False))