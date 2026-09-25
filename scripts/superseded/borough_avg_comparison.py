import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load('data/total_traffic_count_2024_manhattan.csv')
m2025 = load('data/total_traffic_count_2025_manhattan.csv')
b2024 = load('data/total_traffic_count_2024_bronx.csv')
b2025 = load('data/total_traffic_count_2025_bronx.csv')

labels = ['Manhattan', 'Bronx']
vals_2024 = [m2024['vol'].mean(), b2024['vol'].mean()]
vals_2025 = [m2025['vol'].mean(), b2025['vol'].mean()]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, vals_2024, width, label='2024')
ax.bar(x + width/2, vals_2025, width, label='2025')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Average Vehicle Count')
ax.set_title('Average Traffic per Reading: Manhattan vs Bronx, 2024 vs 2025')
ax.legend()

plt.savefig('outputs/borough_avg_comparison.png')