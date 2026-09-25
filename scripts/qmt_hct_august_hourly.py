import requests
import pandas as pd
import matplotlib.pyplot as plt

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

PLAZAS = {27: "Queens Midtown Tunnel", 28: "Hugh L. Carey Tunnel"}

for plaza_id, name in PLAZAS.items():
    fig, ax = plt.subplots()

    # 2024 from MTA data
    where = (
        f"plaza_id = '{plaza_id}' AND direction = 'I' AND "
        f"date between '2024-08-05T00:00:00' and '2024-08-11T23:59:59'"
    )
    resp = requests.get(BNT_URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())
    df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
    df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
    df['total'] = df['vehicles_e_zpass'] + df['vehicles_vtoll']
    df['hour'] = pd.to_numeric(df['hour'], errors='coerce')
    by_hour_2024 = df.groupby('hour')['total'].mean()
    ax.plot(by_hour_2024.index, by_hour_2024.values, label='2024')

    # 2025 and 2026 from CRZ data (MTA stopped in April 2025)
    for year in [2025, 2026]:
        where = (
            f"detection_group = '{name}' AND "
            f"toll_date between '{year}-08-05T00:00:00' and '{year}-08-11T23:59:59'"
        )
        resp = requests.get(CRZ_URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())
        df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce')
        df['hour_of_day'] = pd.to_numeric(df['hour_of_day'], errors='coerce')

        # sum per day first, THEN average across days (same fix as before)
        daily = df.groupby(['toll_date', 'hour_of_day'])['crz_entries'].sum().reset_index()
        by_hour = daily.groupby('hour_of_day')['crz_entries'].mean()
        ax.plot(by_hour.index, by_hour.values, label=str(year))

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Vehicles (inbound, per typical day)')
    ax.set_title(f'{name}: Hourly Traffic, August 2024 vs 2025 vs 2026')
    ax.legend()

    filename = name.lower().replace(' ', '_').replace('.', '')
    plt.savefig(f'outputs/{filename}_august_hourly.png')
    print(f"Chart saved to outputs/{filename}_august_hourly.png")