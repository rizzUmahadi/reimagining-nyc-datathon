import pandas as pd
import matplotlib.pyplot as plt

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

b2024 = load('data/total_traffic_count_2024_bronx.csv')
b2025 = load('data/total_traffic_count_2025_bronx.csv')

by_hour_2024 = b2024.groupby('hh')['vol'].mean()
by_hour_2025 = b2025.groupby('hh')['vol'].mean()

pct_change = (by_hour_2025 - by_hour_2024) / by_hour_2024 * 100

print("Bronx — hour by hour, 2024 vs 2025:")
for hour in range(24):
    print(f"  Hour {hour:2d}: {by_hour_2024[hour]:6.1f} -> {by_hour_2025[hour]:6.1f}  ({pct_change[hour]:+.1f}%)")

fig, ax = plt.subplots()
ax.plot(by_hour_2024.index, by_hour_2024.values, label='2024')
ax.plot(by_hour_2025.index, by_hour_2025.values, label='2025')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Vehicle Count')
ax.set_title('Bronx: Traffic by Hour, 2024 vs 2025')
ax.legend()
plt.savefig('outputs/bronx_hourly_change.png')