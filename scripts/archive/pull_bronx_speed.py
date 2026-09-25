import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"

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

print("Pulling Bronx speed data, Jan 13-19 2024...")
b2024 = fetch_all_rows("borough = 'Bronx' AND data_as_of between '2024-01-13T00:00:00' and '2024-01-19T23:59:59'")
b2024.to_csv('data/bronx_speed_2024.csv', index=False)
print(f"Saved {len(b2024)} rows\n")

print("Pulling Bronx speed data, Jan 13-19 2025...")
b2025 = fetch_all_rows("borough = 'Bronx' AND data_as_of between '2025-01-13T00:00:00' and '2025-01-19T23:59:59'")
b2025.to_csv('data/bronx_speed_2025.csv', index=False)
print(f"Saved {len(b2025)} rows")

# Immediate check: how much do the link_ids actually overlap?
links_2024 = set(b2024['link_id'])
links_2025 = set(b2025['link_id'])
common = links_2024 & links_2025
print(f"\nLink IDs in 2024: {len(links_2024)}")
print(f"Link IDs in 2025: {len(links_2025)}")
print(f"Common link IDs: {len(common)}")
