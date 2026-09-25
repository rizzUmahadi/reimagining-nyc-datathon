import pandas as pd
import matplotlib.pyplot as plt

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load('data/total_traffic_count_2024_manhattan.csv')
m2025 = load('data/total_traffic_count_2025_manhattan.csv')
b2024 = load('data/total_traffic_count_2024_bronx.csv')
b2025 = load('data/total_traffic_count_2025_bronx.csv')

manhattan_all = pd.concat([m2024, m2025])
bronx_all = pd.concat([b2024, b2025])

manhattan_by_hour = manhattan_all.groupby('hh')['vol'].mean()
bronx_by_hour = bronx_all.groupby('hh')['vol'].mean()

print("Manhattan by hour:")
print(manhattan_by_hour)
print("\nBronx by hour:")
print(bronx_by_hour)

fig, ax = plt.subplots()
ax.plot(manhattan_by_hour.index, manhattan_by_hour.values, label='Manhattan')
ax.plot(bronx_by_hour.index, bronx_by_hour.values, label='Bronx')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Vehicle Count')
ax.set_title('Average Traffic by Hour: Manhattan vs Bronx (2024-2025 combined)')
ax.legend()

plt.savefig('outputs/borough_hourly_comparison.png')