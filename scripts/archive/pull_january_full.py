import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/7ym2-wayt.json"

def fetch_all_rows(where_clause, page_size=50000):
    all_rows = []
    offset = 0
    while True:
        params = {"$where": where_clause, "$limit": page_size, "$offset": offset}
        resp = requests.get(URL, params=params)
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

print("Pulling Manhattan, January, 2024-2026...")
df = fetch_all_rows("boro = 'Manhattan' AND m = '1' AND yr in ('2024','2025','2026')")

df.to_csv('data/manhattan_jan_24_25_26_full.csv', index=False)
print(f"\nSaved {len(df)} rows to data/manhattan_jan_24_25_26_full.csv")

print("\nRows per year:")
print(df['yr'].value_counts())
print("\nDistinct segments per year:")
print(df.groupby('yr')['segmentid'].nunique())