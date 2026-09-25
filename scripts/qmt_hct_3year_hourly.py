import requests
import pandas as pd
import matplotlib.pyplot as plt

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

PLAZAS = {27: "Queens Midtown Tunnel", 28: "Hugh L. Carey Tunnel"}
CRZ_NAMES = {"Queens Midtown Tunnel": "Queens Midtown Tunnel", "Hugh L. Carey Tunnel": "Hugh L. Carey Tunnel"}

for plaza_id, name in PLAZAS.items():
    fig, ax = plt.subplots()

    for year, (start, end) in [(2024, ("2024-01-05", "2024-01-11")), (2025, ("2025-01-05", "2025-01-11"))]:
        where = (
            f"plaza_id = '{plaza_id}' AND direction = 'I' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        df['total'] = df['vehicles_e_zpass'] + df['vehicles_vtoll']
        df['hour'] = pd.to_numeric(df['hour'], errors='coerce')

        by_hour = df.groupby('hour')['total'].mean()
        ax.plot(by_hour.index, by_hour.values, label=str(year))

    # 2026: sum PER DAY first, THEN average across the 7 days — matching what the other two years do
    where_2026 = (
        f"detection_group = '{CRZ_NAMES[name]}' AND "
        f"toll_date between '2026-01-05T00:00:00' and '2026-01-11T23:59:59'"
    )
    resp = requests.get(CRZ_URL, params={"$where": where_2026, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce')
    df['hour_of_day'] = pd.to_numeric(df['hour_of_day'], errors='coerce')

    daily_totals = df.groupby(['toll_date', 'hour_of_day'])['crz_entries'].sum().reset_index()
    by_hour_2026 = daily_totals.groupby('hour_of_day')['crz_entries'].mean()
    ax.plot(by_hour_2026.index, by_hour_2026.values, label='2026')

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Vehicles (inbound, per typical day)')
    ax.set_title(f'{name}: Hourly Traffic, 2024 vs 2025 vs 2026')
    ax.legend()

    filename = name.lower().replace(' ', '_').replace('.', '')
    plt.savefig(f'outputs/{filename}_3year_hourly.png')