import matplotlib.pyplot as plt
import numpy as np

data = {
    "RFK Bridge (Bronx)": {"Jan": [195.26, 205.26, 206.03], "Aug": [214.66, 220.18, 220.51]},
    "Bronx-Whitestone": {"Jan": [189.03, 192.28, 200.03], "Aug": [209.92, 218.02, 209.78]},
    "Throgs Neck": {"Jan": [160.79, 171.68, 167.10], "Aug": [183.66, 191.40, 192.10]},
}

facilities = list(data.keys())
years = ['2024', '2025', '2026']
x = np.arange(len(facilities))
width = 0.25

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

for ax, month in zip(axes, ['Jan', 'Aug']):
    for i, year in enumerate(years):
        vals = [data[f][month][i] for f in facilities]
        bars = ax.bar(x + (i-1)*width, vals, width, label=year)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                     f'{val:.0f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(facilities, rotation=15, ha='right')
    ax.set_title(f'{month} 5-11')
    ax.set_ylabel('Average Vehicles per Reading')
    ax.legend()

fig.suptitle('Bronx-Connecting MTA Crossings: Avg Traffic, 2024 vs 2025 vs 2026')
plt.tight_layout()
plt.savefig('outputs/bronx_crossings_verified.png')
print("Chart saved to outputs/bronx_crossings_verified.png")