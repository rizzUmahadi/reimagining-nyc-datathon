"""
Pulls historical daily PM2.5 observations from the AirNow API for a handful
of key NYC locations, so we have current (2025-2026) air quality data even
if NYCCAS on NYC Open Data turns out to be stale.

Requires: pip install python-dotenv requests pandas
Requires a .env file (NOT committed to git) containing:
    AIRNOW_API_KEY=your_key_here
"""

import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("AIRNOW_API_KEY")

if not API_KEY:
    raise SystemExit("AIRNOW_API_KEY not found — check your .env file exists and is filled in.")

# Key NYC locations to track — includes CBD (inside CRZ) and South Bronx
# ("Asthma Alley") for the equity comparison the prompt asks about.
LOCATIONS = {
    "Manhattan_CBD": (40.758, -73.985),      # Midtown, inside congestion zone
    "South_Bronx": (40.816, -73.923),        # Mott Haven / Asthma Alley
    "Upper_Manhattan": (40.824, -73.943),    # outside CRZ, comparison point
    "Downtown_Brooklyn": (40.693, -73.986),  # crossing-adjacent borough
}

BASE_URL = "https://www.airnowapi.org/aq/observation/latLong/historical/"

def fetch_pm25(lat, lon, date_str):
    """date_str format: 'YYYY-MM-DDT00-0000'"""
    params = {
        "format": "application/json",
        "latitude": lat,
        "longitude": lon,
        "date": date_str,
        "distance": 25,
        "API_KEY": API_KEY,
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

# Pull one sample date first to confirm the API key and data actually work
# before looping over a full date range.
test_date = "2026-09-01T00-0000"
sample = fetch_pm25(*LOCATIONS["Manhattan_CBD"], test_date)
print("=== Sample response for Manhattan CBD, Sept 1 2026 ===")
print(sample)

# If that looks good, pull a real before/after comparison:

DATES_EARLY = pd.date_range("2025-01-13", "2025-01-19")
DATES_RECENT = pd.date_range("2026-08-25", "2026-08-31")

rows = []
for label, dates in [("early", DATES_EARLY), ("recent", DATES_RECENT)]:
    for loc_name, (lat, lon) in LOCATIONS.items():
        for d in dates:
            date_str = d.strftime("%Y-%m-%dT00-0000")
            try:
                data = fetch_pm25(lat, lon, date_str)
                for entry in data:
                    if entry.get("ParameterName") != "PM2.5":
                        continue
                    entry["location_label"] = loc_name
                    entry["period_label"] = label
                    rows.append(entry)
            except Exception as e:
                print(f"Failed for {loc_name} {date_str}: {e}")
            time.sleep(0.2)  # be polite to the API

df = pd.DataFrame(rows)
df.to_csv("data/airnow_pm25_comparison.csv", index=False)
print(f"Saved {len(df)} rows to data/airnow_pm25_comparison.csv")

# Critical check: how many actually distinct monitor locations did we get back?
if not df.empty:
    print("\n=== Distinct reporting areas / coordinates returned ===")
    print(df[["ReportingArea", "Latitude", "Longitude"]].drop_duplicates())
