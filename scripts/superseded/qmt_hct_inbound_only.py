import requests
import pandas as pd

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"

PLAZAS = {27: "Queens Midtown Tunnel", 28: "Hugh L. Carey Tunnel"}

for plaza_id, name in PLAZAS.items():
    print(f"\n{name}:")
    for year, (start, end) in [(2024, ("2024-01-05", "2024-01-11")), (2025, ("2025-01-05", "2025-01-11"))]:
        where = (
            f"plaza_id = '{plaza_id}' AND direction = 'I' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        print(f"  {year}: {len(df)} rows (inbound only)")
        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        total = (df['vehicles_e_zpass'] + df['vehicles_vtoll']).sum()
        print(f"  {year} inbound total: {total:,.0f}")