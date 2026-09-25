import pandas as pd
import requests

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

for year in ['2024', '2025', '2026']:
    df = fetch_all_rows(f"boro = 'Bronx' AND yr = '{year}'")
    if df.empty:
        print(f"{year}: NO DATA")
        continue
    months = sorted(df['m'].astype(int).unique())
    print(f"{year}: months covered = {months}")