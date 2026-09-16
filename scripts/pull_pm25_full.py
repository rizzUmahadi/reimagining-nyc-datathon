"""
Pulls the FULL NYCCAS PM2.5 2024 dataset, filtered to Community District
level only (the dataset mixes CD, borough, and citywide rows together —
we need one consistent geographic level for the map).
"""

import pandas as pd
import requests

AQ_URL = "https://data.cityofnewyork.us/resource/c3uy-2p5r.json"

params = {
    "$where": "name = 'Fine particles (PM 2.5)' AND time_period = '2024' AND geo_type_name = 'CD'",
    "$limit": 500,
}
resp = requests.get(AQ_URL, params=params)
df = pd.DataFrame(resp.json())

df.to_csv("data/pm25_2024.csv", index=False)
print(f"Saved {len(df)} rows to data/pm25_2024.csv")
print(f"\nCovers {df['geo_place_name'].nunique()} distinct community districts")
print(df[["geo_place_name", "data_value"]].sort_values("data_value", ascending=False).head(10))
