import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/7ym2-wayt.json"

for label, year, month in [("Jan 2024", "2024", "1"), ("Jan 2026", "2026", "1"), ("Sep 2024", "2024", "9"), ("Sep 2025", "2025", "9")]:
    resp = requests.get(URL, params={
        "$select": "distinct segmentid, street",
        "$where": f"boro = 'Bronx' AND yr = '{year}' AND m = '{month}'",
        "$limit": 20,
    })
    df = pd.DataFrame(resp.json())
    print(f"\n{label}:")
    print(df.to_string(index=False))