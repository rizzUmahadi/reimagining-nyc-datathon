import pandas as pd
import matplotlib.pyplot as plt

b2024 = pd.read_csv('data/bronx_speed_2024.csv')
b2025 = pd.read_csv('data/bronx_speed_2025.csv')

b2024['speed'] = pd.to_numeric(b2024['speed'], errors='coerce')
b2025['speed'] = pd.to_numeric(b2025['speed'], errors='coerce')

common_links = set(b2024['link_id']) & set(b2025['link_id'])
b2024_clean = b2024[(b2024['link_id'].isin(common_links)) & (b2024['status'] == 0)]
b2025_clean = b2025[(b2025['link_id'].isin(common_links)) & (b2025['status'] == 0)]

avg_2024 = b2024_clean['speed'].mean()
avg_2025 = b2025_clean['speed'].mean()
change = (avg_2025 - avg_2024) / avg_2024 * 100

print(f"Bronx average speed: {avg_2024:.2f} mph -> {avg_2025:.2f} mph ({change:+.2f}%)")

fig, ax = plt.subplots()
bars = ax.bar(['2024', '2025'], [avg_2024, avg_2025], color=['tab:blue', 'tab:orange'])

for bar, val in zip(bars, [avg_2024, avg_2025]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{val:.2f} mph', ha='center', va='bottom')

ax.set_ylabel('Average Speed (mph)')
ax.set_title('Bronx: Average Traffic Speed, 2024 vs 2025 (matched sensors)')
plt.savefig('outputs/bronx_speed_compare.png')