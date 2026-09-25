import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/bronx_pm25_epa_2024_2025_2026.csv')
pivot = df.groupby(['local_site_name', 'Year'])['arithmetic_mean'].mean().unstack()

sites = pivot.index.tolist()
years = [2024, 2025, 2026]
x = np.arange(len(sites))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
for i, year in enumerate(years):
    vals = pivot[year].values
    bars = ax.bar(x + (i-1)*width, vals, width, label=str(year))
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{val:.1f}', ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(sites)
ax.set_ylabel('PM2.5 (µg/m³)')
ax.set_title('Bronx PM2.5 by EPA Monitor: Jan-Jul, 2024 vs 2025 vs 2026')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/bronx_pm25_epa_chart.png')
print("Chart saved to outputs/bronx_pm25_epa_chart.png")