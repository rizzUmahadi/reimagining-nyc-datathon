import requests
import pandas as pd

# ---------------------------------------------------------------------------
# PART 1: 2024 and 2025 from the MTA B&T dataset (real toll vehicle counts)
# ---------------------------------------------------------------------------
BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"

PLAZAS = {
    27: "Queens Midtown Tunnel",
    28: "Hugh L. Carey Tunnel",
}

results = {"Queens Midtown Tunnel": {}, "Hugh L. Carey Tunnel": {}}

for plaza_id, name in PLAZAS.items():
    for year, (start, end) in [(2024, ("2024-01-05", "2024-01-11")), (2025, ("2025-01-05", "2025-01-11"))]:
        where = (
            f"plaza_id = '{plaza_id}' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        total = (df['vehicles_e_zpass'] + df['vehicles_vtoll']).sum()
        results[name][year] = total

# ---------------------------------------------------------------------------
# PART 2: 2026 from the CRZ Vehicle Entries dataset (live, current data)
# ---------------------------------------------------------------------------
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

CRZ_NAMES = {
    "Queens Midtown Tunnel": "Queens Midtown Tunnel",
    "Hugh L. Carey Tunnel": "Hugh L. Carey Tunnel",
}

for display_name, detection_group in CRZ_NAMES.items():
    where = (
        f"detection_group = '{detection_group}' AND "
        f"toll_date between '2026-01-05T00:00:00' and '2026-01-11T23:59:59'"
    )
    resp = requests.get(CRZ_URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    if df.empty:
        results[display_name][2026] = None
        continue
    df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce')
    results[display_name][2026] = df['crz_entries'].sum()

# ---------------------------------------------------------------------------
# PRINT COMBINED RESULTS
# ---------------------------------------------------------------------------
for name, years in results.items():
    print(f"\n{name}:")
    for year in [2024, 2025, 2026]:
        val = years.get(year)
        if val is None:
            print(f"  {year}: NO DATA")
        else:
            print(f"  {year}: {val:,.0f}")