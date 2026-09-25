import requests
import pandas as pd
import matplotlib.pyplot as plt

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

LINK_IDS = [4329472, 4329507, 4329508, 4456511, 4329473]
link_filter = " OR ".join([f"link_id = '{lid}'" for lid in LINK_IDS])

YEARS = {
    2024: ("2024-01-05", "2024-01-11"),
    2025: ("2025-01-05", "2025-01-11"),
    2026: ("2026-01-05", "2026-01-11"),
}

labels = []
speeds = []

for year, (start, end) in YEARS.items():
    where = (
        f"({link_filter}) AND "
        f"data_as_of between '{start}T00:00:00' and '{end}T23:59:59' AND "
        f"status = '0'"
    )
    resp = requests.get(URL, params={"$where": where, "$limit": 50000})
    df = pd.DataFrame(resp.json())

    if df.empty:
        print(f"{year}: NO DATA — skipping")
        continue

    df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
    avg_speed = df['speed'].mean()
    print(f"{year}: {len(df)} readings, average speed = {avg_speed:.2f} mph")

    labels.append(str(year))
    speeds.append(avg_speed)

if not speeds:
    print("\nNo data found for ANY year — nothing to chart.")
else:
    fig, ax = plt.subplots()
    bars = ax.bar(labels, speeds, color='tab:blue')

    for bar, val in zip(bars, speeds):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{val:.1f} mph', ha='center', va='bottom')

    ax.set_ylabel('Average Speed (mph)')
    ax.set_title('Lincoln Tunnel + Queens Midtown Tunnel: Avg Speed by Year')
    plt.savefig('outputs/lincoln_qmt_yearly.png')
    print("\nChart saved to outputs/lincoln_qmt_yearly.png")