import pandas as pd
import matplotlib.pyplot as plt

def load_and_normalize(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load_and_normalize('data/total_traffic_count_2024_manhattan.csv')
m2025 = load_and_normalize('data/total_traffic_count_2025_manhattan.csv')

avg_2024 = m2024.groupby('hh')['vol'].mean()
avg_2025 = m2025.groupby('hh')['vol'].mean()

print("Manhattan 2024:")
print(avg_2024)
print("\nManhattan 2025:")
print(avg_2025)

plt.plot(avg_2024.index, avg_2024.values, label='2024')
plt.plot(avg_2025.index, avg_2025.values, label='2025')
plt.xlabel('Hour of Day')
plt.ylabel('Average Vehicle Count')
plt.title('Manhattan: Average Traffic by Hour, 2024 vs 2025')
plt.legend()
plt.savefig('outputs/hourly_avg_manhattan.png')