# reimagining-nyc-datathon
## Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt




You also need a `.env` file in the repo root (this is gitignored — you must
create your own, it won't come through git clone):


## How to run everything, in order
source venv/bin/activate # every new terminal session

python scripts/check_data_availability.py # pulls traffic CSVs (skips if already present)
python scripts/pull_pm25_full.py # pulls PM2.5 2024 CSV
python scripts/pull_airnow_data.py # pulls AirNow comparison (needs .env)
python scripts/build_map_v1.py # builds the actual map


Then view the map — Python's built-in web server is required because opening
the HTML file directly gets blocked by OpenStreetMap's tile policy:

cd outputs
python3 -m http.server 8000


Open `http://localhost:8000/draft_map.html` in your browser.



## What the map shows

- **Choropleth (yellow → red by district):** PM2.5 annual average, 2024 —
  this is the most recent year NYC's official air quality dataset (NYCCAS)
  has published. There's no 2025/2026 data yet, so this is a spatial
  snapshot, not a live before/after comparison.
- **Circle markers at crossings:** % change in traffic volume, comparing the
  week of Jan 13–19, 2025 (right after congestion pricing launched) to the
  week of Aug 25–31, 2026 (most recent full week available). Red = traffic
  increased at that crossing, blue = decreased. Size = magnitude of change.

## Known limitations (already figured out — no need to re-investigate)

- NYCCAS PM2.5 data stops at 2024, so it can't show "after congestion
  pricing" directly — it's paired with the traffic data (which does cover
  before/after) as a spatial reference layer instead.
- AirNow (EPA real-time air quality) was tested as a fix for the above, but
  only resolves NYC into ~2 broad regions — not granular enough to compare
  neighborhoods like South Bronx vs. Manhattan. It's saved in
  `data/airnow_pm25_comparison.csv` but isn't used in the map yet.
- Traffic crossing coordinates are manually placed (approximate), since the
  MTA dataset doesn't include lat/lon directly.

## Data sources

- Traffic: MTA Congestion Relief Zone Vehicle Entries (`data.ny.gov`,
  dataset `t6yz-b64h`), pulled live via API — see
  `scripts/check_data_availability.py`.
- Air quality: NYC NYCCAS PM2.5 (`data.cityofnewyork.us`, dataset
  `c3uy-2p5r`), pulled via API — see `scripts/pull_pm25_full.py`.
- Boundaries: NYC Community Districts (`data.cityofnewyork.us`, dataset
  `5crt-au7u`).