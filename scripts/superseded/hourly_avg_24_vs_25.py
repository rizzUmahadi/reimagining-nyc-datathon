import pandas as pd
import matplotlib.pyplot as plt

def load_and_normalize(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]  # make all column names lowercase
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load_and_normalize('data/total_traffic_count_2024_manhattan.csv')
m2025 = load_and_normalize('data/total_traffic_count_2025_manhattan.csv')
b2024 = load_and_normalize('data/total_traffic_count_2024_bronx.csv')
b2025 = load_and_normalize('data/total_traffic_count_2025_bronx.csv')

combined_2024 = pd.concat([m2024, b2024])
combined_2025 = pd.concat([m2025, b2025])

avg_by_hour_2024 = combined_2024.groupby('hh')['vol'].mean()
avg_by_hour_2025 = combined_2025.groupby('hh')['vol'].mean()

print("=== Average vehicles per 15-min interval, by hour ===")
print("2024:")
print(avg_by_hour_2024)
print("\n2025:")
print(avg_by_hour_2025)

plt.plot(avg_by_hour_2024.index, avg_by_hour_2024.values, label='2024')
plt.plot(avg_by_hour_2025.index, avg_by_hour_2025.values, label='2025')
plt.xlabel('Hour of Day')
plt.ylabel('Average Vehicle Count')
plt.title('Average Traffic by Hour: 2024 vs 2025 (Manhattan + Bronx)')
plt.legend()
plt.savefig('outputs/hourly_avg_24_vs_25.png')