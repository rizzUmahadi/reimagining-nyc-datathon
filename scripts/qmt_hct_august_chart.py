import matplotlib.pyplot as plt
import numpy as np

data = {
    "Queens Midtown Tunnel": {2024: 309230, 2025: 315539, 2026: 295194},
    "Hugh L. Carey Tunnel": {2024: 216027, 2025: 147274, 2026: 130790},
}

labels = list(data.keys())
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()

for i, year in enumerate([2024, 2025, 2026]):
    vals = [data[name][year] for name in labels]
    bars = ax.bar(x + (i-1)*width, vals, width, label=str(year))
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{int(val):,}', ha='center', va='bottom', fontsize=7, rotation=90)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Inbound Vehicles (Aug 5-11)')
ax.set_title('QMT & HCT: August 2024 vs 2025 vs 2026 (verified)')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/qmt_hct_august_yearly.png')
print("Chart saved to outputs/qmt_hct_august_yearly.png")