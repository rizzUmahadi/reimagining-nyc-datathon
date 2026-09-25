import pandas as pd
import matplotlib.pyplot as plt

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load('data/total_traffic_count_2024_manhattan.csv')
m2025 = load('data/total_traffic_count_2025_manhattan.csv')

m2024['key'] = list(zip(m2024['segmentid'], m2024['m'], m2024['d'], m2024['hh'], m2024['mm'], m2024['direction']))
m2025['key'] = list(zip(m2025['segmentid'], m2025['m'], m2025['d'], m2025['hh'], m2025['mm'], m2025['direction']))

common_keys = set(m2024['key']) & set(m2025['key'])
m2024_exact = m2024[m2024['key'].isin(common_keys)]
m2025_exact = m2025[m2025['key'].isin(common_keys)]

by_hour_2024 = m2024_exact.groupby('hh')['vol'].mean()
by_hour_2025 = m2025_exact.groupby('hh')['vol'].mean()

print("Hour-by-hour, exact matched data:")
for hour in range(24):
    v24 = by_hour_2024.get(hour, float('nan'))
    v25 = by_hour_2025.get(hour, float('nan'))
    print(f"  Hour {hour:2d}: {v24:6.1f} -> {v25:6.1f}")

fig, ax = plt.subplots()
ax.plot(by_hour_2024.index, by_hour_2024.values, label='2024')
ax.plot(by_hour_2025.index, by_hour_2025.values, label='2025')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Vehicle Count')
ax.set_title('Manhattan: EXACT Matched Traffic by Hour, 2024 vs 2025')
ax.legend()
plt.savefig('outputs/manhattan_final_match.png')