import requests
import pandas as pd

URL = "https://data.ny.gov/resource/qzve-kjga.json"

PLAZAS = {
    27: "Queens Midtown Tunnel",
    28: "Hugh L. Carey Tunnel",
}

YEARS = {
    2024: ("2024-01-05", "2024-01-11"),
    2025: ("2025-01-05", "2025-01-11"),
    2026: ("2026-01-05", "2026-01-11"),
}

for plaza_id, name in PLAZAS.items():
    print(f"\n=== {name} (plaza_id {plaza_id}) ===")
    for year, (start, end) in YEARS.items():
        where = (
            f"plaza_id = '{plaza_id}' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())

        if df.empty:
            print(f"  {year}: NO DATA")
            continue

        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        total = (df['vehicles_e_zpass'] + df['vehicles_vtoll']).sum()

        print(f"  {year}: {len(df)} rows, total vehicles = {total:,.0f}")