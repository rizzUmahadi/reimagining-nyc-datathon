import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

PLAZAS = {27: "Queens Midtown Tunnel", 28: "Hugh L. Carey Tunnel"}

results = {"Queens Midtown Tunnel": {}, "Hugh L. Carey Tunnel": {}}

# 2024 and 2025: MTA data, inbound only
for plaza_id, name in PLAZAS.items():
    for year, (start, end) in [(2024, ("2024-01-05", "2024-01-11")), (2025, ("2025-01-05", "2025-01-11"))]:
        where = (
            f"plaza_id = '{plaza_id}' AND direction = 'I' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        results[name][year] = (df['vehicles_e_zpass'] + df['vehicles_vtoll']).sum()

# 2026: CRZ data (entries only, by definition)
for name in ["Queens Midtown Tunnel", "Hugh L. Carey Tunnel"]:
    where = f"detection_group = '{name}' AND toll_date between '2026-01-05T00:00:00' and '2026-01-11T23:59:59'"
    resp = requests.get(CRZ_URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce')
    results[name][2026] = df['crz_entries'].sum()

# Print to terminal
print("=== FINAL VERIFIED NUMBERS ===")
for name, years in results.items():
    print(f"\n{name}:")
    for year in [2024, 2025, 2026]:
        print(f"  {year}: {years[year]:,.0f}")

# Chart
labels = list(results.keys())
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
for i, year in enumerate([2024, 2025, 2026]):
    vals = [results[name][year] for name in labels]
    bars = ax.bar(x + (i-1)*width, vals, width, label=str(year))
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{int(val):,}', ha='center', va='bottom', fontsize=7, rotation=90)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Inbound Vehicles (Jan 5-11)')
ax.set_title('QMT & HCT: 2024 vs 2025 vs 2026 (inbound only, verified)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/qmt_hct_final_3year.png')
print("\nChart saved to outputs/qmt_hct_final_3year.png")