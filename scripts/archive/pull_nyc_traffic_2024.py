"""
Pulls NYC DOT Automated Traffic Volume Counts for the WHOLE city, 2024 only.
Same dataset your teammate's borough-specific files came from (ID 7ym2-wayt),
just without filtering to one borough.
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

print("Pulling all NYC traffic counts for 2024 (this may take a few minutes)...")
df = fetch_all_rows(URL, "yr = '2024'")

df.to_csv("data/total_traffic_count_2024_nyc.csv", index=False)
print(f"\nSaved {len(df)} rows to data/total_traffic_count_2024_nyc.csv")
print(f"Boroughs covered: {df['boro'].unique().tolist()}")
