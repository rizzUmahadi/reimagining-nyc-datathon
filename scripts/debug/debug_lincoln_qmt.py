import requests
import pandas as pd

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

LINK_IDS = [4329472, 4329507, 4329508, 4456511, 4329473]
link_filter = " OR ".join([f"link_id = {lid}" for lid in LINK_IDS])

YEARS = {
    2024: ("2024-01-05", "2024-01-11"),
    2025: ("2025-01-05", "2025-01-11"),
    2026: ("2026-01-05", "2026-01-11"),
}

for year, (start, end) in YEARS.items():
    where = (
        f"({link_filter}) AND "
        f"data_as_of between '{start}T00:00:00' and '{end}T23:59:59' AND "
        f"status = 0"
    )
    resp = requests.get(URL, params={"$where": where, "$limit": 50000})
    print(f"{year}: status code {resp.status_code}")
    df = pd.DataFrame(resp.json())
    print(f"  Rows returned: {len(df)}")
    print(f"  Columns: {df.columns.tolist()}")