import requests
import pandas as pd

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

PLAZAS = {27: "Queens Midtown Tunnel", 28: "Hugh L. Carey Tunnel"}

results = {"Queens Midtown Tunnel": {}, "Hugh L. Carey Tunnel": {}}

# 2024 only from MTA data (last real year this dataset has for August)
for plaza_id, name in PLAZAS.items():
    where = (
        f"plaza_id = '{plaza_id}' AND direction = 'I' AND "
        f"date between '2024-08-05T00:00:00' and '2024-08-11T23:59:59'"
    )
    resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
    df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
    results[name][2024] = (df['vehicles_e_zpass'] + df['vehicles_vtoll']).sum()

# 2025 AND 2026 from CRZ data (since MTA data stops in April 2025)
for name in ["Queens Midtown Tunnel", "Hugh L. Carey Tunnel"]:
    for year in [2025, 2026]:
        where = (
            f"detection_group = '{name}' AND "
            f"toll_date between '{year}-08-05T00:00:00' and '{year}-08-11T23:59:59'"
        )
        resp = requests.get(CRZ_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        if df.empty:
            results[name][year] = None
            continue
        df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce')
        results[name][year] = df['crz_entries'].sum()

print("=== AUGUST 5-11: QMT & HCT, 2024 (MTA) vs 2025/2026 (CRZ) ===")
for name, years in results.items():
    print(f"\n{name}:")
    for year in [2024, 2025, 2026]:
        val = years.get(year)
        print(f"  {year}: {'NO DATA' if val is None else f'{val:,.0f}'}")