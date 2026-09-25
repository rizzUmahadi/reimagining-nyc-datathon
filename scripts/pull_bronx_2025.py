"""
Pulls the CORRECT 2025 Bronx traffic data — fixes the mislabeled file
that actually contained 2024 data.
"""

import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/7ym2-wayt.json"

def fetch_all_rows(url, where_clause, page_size=50000):
    all_rows = []
    offset = 0
    while True:
        params = {"$where": where_clause, "$limit": page_size, "$offset": offset}
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        all_rows.extend(batch)
        print(f"  ...fetched {len(all_rows)} rows so far")
        offset += page_size
        if len(batch) < page_size:
            break
    return pd.DataFrame(all_rows)

print("Pulling Bronx traffic counts for 2025...")
df = fetch_all_rows(URL, "yr = '2025' AND boro = 'Bronx'")

df.to_csv("data/total_traffic_count_2025_bronx_FIXED.csv", index=False)
print(f"\nSaved {len(df)} rows to data/total_traffic_count_2025_bronx_FIXED.csv")
print(f"Years present: {df['yr'].unique().tolist()}")
