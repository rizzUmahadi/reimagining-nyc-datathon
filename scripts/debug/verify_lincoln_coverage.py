import requests
import pandas as pd

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

LINCOLN_LINK_IDS = [4329472, 4329507, 4329508, 4329473]
link_filter = " OR ".join([f"link_id = '{lid}'" for lid in LINCOLN_LINK_IDS])

WEEKS = {
    "Jan 2024": ("2024-01-05", "2024-01-11"),
    "Jan 2025": ("2025-01-05", "2025-01-11"),
    "Jan 2026": ("2026-01-05", "2026-01-11"),
    "Aug 2024": ("2024-08-05", "2024-08-11"),
    "Aug 2025": ("2025-08-05", "2025-08-11"),
    "Aug 2026": ("2026-08-05", "2026-08-11"),
}

for label, (start, end) in WEEKS.items():
    where = (
        f"({link_filter}) AND status = '0' AND "
        f"data_as_of between '{start}T00:00:00' and '{end}T23:59:59'"
    )
    resp = requests.get(URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    print(f"{label}: {len(df)} rows")