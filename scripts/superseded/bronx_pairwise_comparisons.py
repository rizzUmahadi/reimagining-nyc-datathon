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
        offset += page_size
        if len(batch) < page_size:
            break
    return pd.DataFrame(all_rows)

print("=== COMPARISON 1: January, 2024 vs 2026 ===")
for year in ['2024', '2026']:
    df = fetch_all_rows(f"boro = 'Bronx' AND yr = '{year}' AND m = '1'")
    if df.empty:
        print(f"  {year}: NO DATA")
        continue
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    print(f"  {year}: {len(df)} rows, {df['segmentid'].nunique()} segments, avg vehicles/reading = {df['vol'].mean():.2f}")

print("\n=== COMPARISON 2: September, 2024 vs 2025 ===")
for year in ['2024', '2025']:
    df = fetch_all_rows(f"boro = 'Bronx' AND yr = '{year}' AND m = '9'")
    if df.empty:
        print(f"  {year}: NO DATA")
        continue
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    print(f"  {year}: {len(df)} rows, {df['segmentid'].nunique()} segments, avg vehicles/reading = {df['vol'].mean():.2f}")