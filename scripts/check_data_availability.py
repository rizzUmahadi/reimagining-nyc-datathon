"""
Step 1: Pull real data via the Socrata API (filtered, not full downloads)
and check what date ranges are actually available.

Run this FIRST before building anything else — it tells you what data
you actually have to work with.
"""

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# 1. AIR QUALITY (NYCCAS PM2.5) — check what time periods exist
# ---------------------------------------------------------------------------
# Confirmed real columns: Unique ID, Indicator ID, Name, Measure, Measure Info,
# Geo Type Name, Geo Join ID, Geo Place Name, Time Period, Start_Date,
# Data Value, Message

AQ_URL = "https://data.cityofnewyork.us/resource/c3uy-2p5r.json"

# Pull just PM2.5 rows, sorted by most recent Start_Date, to see how current the data is
params = {
    "$where": "name = 'Fine particles (PM 2.5)'",
    "$order": "start_date DESC",
    "$limit": 20,
}
resp = requests.get(AQ_URL, params=params)
aq_recent = pd.DataFrame(resp.json())

print("=== Most recent PM2.5 records available ===")
if not aq_recent.empty:
    print(aq_recent[["name", "geo_place_name", "time_period", "start_date", "data_value"]])
else:
    print("Still nothing — checking actual 'name' values in this dataset instead:")
    params2 = {"$select": "distinct name", "$limit": 50}
    resp2 = requests.get(AQ_URL, params=params2)
    raw = pd.DataFrame(resp2.json())
    print(raw["name"].tolist() if not raw.empty else "Dataset returned nothing at all — ID may be wrong.")

# ---------------------------------------------------------------------------
# 2. TRAFFIC (MTA CRZ Vehicle Entries) — pull a filtered sample, not the full 600MB file
# ---------------------------------------------------------------------------
TRAFFIC_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

params = {
    "$order": "toll_date DESC",
    "$limit": 20,
}
resp = requests.get(TRAFFIC_URL, params=params)
traffic_recent = pd.DataFrame(resp.json())

print("\n=== Most recent traffic entries available ===")
if not traffic_recent.empty:
    print(traffic_recent.columns.tolist())
    print(traffic_recent[["toll_date", "detection_group", "detection_region", "vehicle_class", "crz_entries"]].head(10))
else:
    print("No traffic rows returned — check field names via the dataset's API docs page.")

# Confirmed columns as of Sept 2026:
# toll_date, toll_hour, toll_10_minute_block, minute_of_hour, hour_of_day,
# day_of_week_int, day_of_week, toll_week, time_period, vehicle_class,
# detection_group, detection_region, crz_entries, excluded_roadway_entries

# ---------------------------------------------------------------------------
# 3. Once you've confirmed real date ranges above, pull your actual working sets
#    Example: traffic for two specific weeks to compare
# ---------------------------------------------------------------------------
# Traffic data confirmed live through Sept 5, 2026 — use these real windows:
EARLY_WEEK = ("2025-01-13", "2025-01-19")    # first full week after launch (Jan 5, 2025)
RECENT_WEEK = ("2026-08-25", "2026-08-31")   # most recent full week available

def fetch_all_rows(url, where_clause, page_size=50000):
    """Paginate through Socrata results instead of silently truncating at one page."""
    all_rows = []
    offset = 0
    while True:
        params = {"$where": where_clause, "$limit": page_size, "$offset": offset}
        resp = requests.get(url, params=params)
        batch = resp.json()
        if not batch:
            break
        all_rows.extend(batch)
        offset += page_size
        if len(batch) < page_size:
            break
    return pd.DataFrame(all_rows)

for label, (start, end) in [("early", EARLY_WEEK), ("recent", RECENT_WEEK)]:
    out_path = f"data/traffic_{label}_week.csv"
    if pd.io.common.file_exists(out_path):
        print(f"{out_path} already exists — skipping re-download.")
        continue
    where = f"toll_date between '{start}T00:00:00' and '{end}T23:59:59'"
    data = fetch_all_rows(TRAFFIC_URL, where)
    data.to_csv(out_path, index=False)
    print(f"Saved {len(data)} rows to {out_path}")
