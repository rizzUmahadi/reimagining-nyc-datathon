import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/manhattan_pm25_epa_2024_2025_2026.csv')
pivot = df.groupby(['local_site_name', 'Year'])['arithmetic_mean'].mean().unstack()

# CHART 1: 2024 vs 2025, only sites with both years (PS 19, IS 45)
sites_a = ['PS 19', 'IS 45']
fig, ax = plt.subplots(figsize=(8, 6))
x = np.arange(len(sites_a))
width = 0.35
vals_2024 = [pivot.loc[s, 2024] for s in sites_a]
vals_2025 = [pivot.loc[s, 2025] for s in sites_a]
bars1 = ax.bar(x - width/2, vals_2024, width, label='2024')
bars2 = ax.bar(x + width/2, vals_2025, width, label='2025')
for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.1f}', ha='center', va='bottom')
ax.set_xticks(x)
ax.set_xticklabels(sites_a)
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_title('Manhattan PM2.5: 2024 vs 2025 (sites with both years)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/manhattan_pm25_2024_2025.png')
print("Saved outputs/manhattan_pm25_2024_2025.png")

# CHART 2: 2025 vs 2026, only sites with both years (CCNY, Division Street, PS 19)
sites_b = ['CCNY', 'DIVISION STREET', 'PS 19']
fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(len(sites_b))
vals_2025b = [pivot.loc[s, 2025] for s in sites_b]
vals_2026b = [pivot.loc[s, 2026] for s in sites_b]
bars1 = ax.bar(x - width/2, vals_2025b, width, label='2025')
bars2 = ax.bar(x + width/2, vals_2026b, width, label='2026')
for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.1f}', ha='center', va='bottom')
ax.set_xticks(x)
ax.set_xticklabels(sites_b)
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_title('Manhattan PM2.5: 2025 vs 2026 (sites with both years)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/manhattan_pm25_2025_2026.png')
print("Saved outputs/manhattan_pm25_2025_2026.png")