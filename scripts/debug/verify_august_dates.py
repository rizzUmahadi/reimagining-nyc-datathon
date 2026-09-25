import requests
import pandas as pd

CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

for name in ["Queens Midtown Tunnel", "Hugh L. Carey Tunnel"]:
    for year in [2025, 2026]:
        where = (
            f"detection_group = '{name}' AND "
            f"toll_date between '{year}-08-05T00:00:00' and '{year}-08-11T23:59:59'"
        )
        resp = requests.get(CRZ_URL, params={"$select": "distinct toll_date", "$where": where, "$limit": 50})
        df = pd.DataFrame(resp.json())
        dates = sorted(df['toll_date'].unique()) if not df.empty else []
        print(f"{name} {year}: {len(dates)} distinct dates")
        print(f"  {dates}")