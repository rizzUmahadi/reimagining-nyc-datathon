import requests
import pandas as pd

URL = "https://data.ny.gov/resource/ebfx-2m7v.json"

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

FACILITIES = ["Robert F. Kennedy Bridge Bronx", "Bronx - Whitestone Bridge", "Throgs Neck Bridge"]
WEEKS = {
    ("Jan", 2024): ("2024-01-05", "2024-01-11"),
    ("Jan", 2025): ("2025-01-05", "2025-01-11"),
    ("Jan", 2026): ("2026-01-05", "2026-01-11"),
    ("Aug", 2024): ("2024-08-05", "2024-08-11"),
    ("Aug", 2025): ("2025-08-05", "2025-08-11"),
    ("Aug", 2026): ("2026-08-05", "2026-08-11"),
}

for facility in FACILITIES:
    print(f"\n=== {facility} ===")
    for (label, year), (start, end) in WEEKS.items():
        where = (
            f"facility = '{facility}' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        df = fetch_all_rows(where)
        if df.empty:
            print(f"  {label} {year}: NO DATA")
            continue
        df['traffic_count'] = pd.to_numeric(df['traffic_count'], errors='coerce')
        total = df['traffic_count'].sum()
        print(f"  {label} {year}: {len(df)} rows, total = {total:,.0f}")