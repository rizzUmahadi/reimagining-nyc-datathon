import requests
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://data.ny.gov/resource/qzve-kjga.json"

PLAZAS = {
    27: "Queens Midtown Tunnel",
    28: "Hugh L. Carey Tunnel",
}

YEARS = {
    2024: ("2024-01-05", "2024-01-11"),
    2025: ("2025-01-05", "2025-01-11"),
}

for plaza_id, name in PLAZAS.items():
    fig, ax = plt.subplots()

    for year, (start, end) in YEARS.items():
        where = (
            f"plaza_id = '{plaza_id}' AND "
            f"date between '{start}T00:00:00' and '{end}T23:59:59'"
        )
        resp = requests.get(URL, params={"$where": where, "$limit": 50000})
        df = pd.DataFrame(resp.json())

        df['vehicles_e_zpass'] = pd.to_numeric(df['vehicles_e_zpass'], errors='coerce')
        df['vehicles_vtoll'] = pd.to_numeric(df['vehicles_vtoll'], errors='coerce')
        df['total'] = df['vehicles_e_zpass'] + df['vehicles_vtoll']
        df['hour'] = pd.to_numeric(df['hour'], errors='coerce')

        by_hour = df.groupby('hour')['total'].mean()

        print(f"\n{name} - {year} by hour:")
        print(by_hour)

        ax.plot(by_hour.index, by_hour.values, label=str(year))

    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Vehicles')
    ax.set_title(f'{name}: Traffic by Hour, 2024 vs 2025')
    ax.legend()

    filename = name.lower().replace(' ', '_')
    plt.savefig(f'outputs/{filename}_hourly.png')
    print(f"Chart saved to outputs/{filename}_hourly.png")