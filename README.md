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
## Viewing the four PM2.5 maps

There are four maps showing air quality by district/monitor:

1. `outputs/map_2024_v2.html` — PM2.5 by community district, 2024
2. `outputs/map_2025_v2.html` — PM2.5 by community district, 2025
3. `outputs/map_2026_v3.html` — PM2.5 at individual EPA monitor sites, 2026
   (Jan-Jul only; full district-level 2026 data doesn't exist yet, so this
   is a point map, not a choropleth — see Known Limitations)
4. `outputs/map_change_2024_2025.html` — the 2024→2025 change, one map,
   colored by how much each district's PM2.5 changed (blue = improved,
   red = worsened). This is the map that actually shows the year-over-year
   story — maps 1 and 2 alone look nearly identical since PM2.5 changes are
   small relative to their absolute levels.

To view any of them, they must be served locally (opening the HTML file
directly is blocked by the map tile provider's policy):

cd outputs
python3 -m http.server 8000

Then open in your browser:
- http://localhost:8000/map_2024_v2.html
- http://localhost:8000/map_2025_v2.html
- http://localhost:8000/map_2026_v3.html
- http://localhost:8000/map_change_2024_2025.html

Note: `outputs/` also contains several older/intermediate map files
(map_2024.html, map_2026_partial.html, map_2026_fixed.html, etc.) from
earlier iterations — the four listed above are the current, correct ones.
