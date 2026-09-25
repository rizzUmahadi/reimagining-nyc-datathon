import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    "Queens Midtown Tunnel": {2024: 511820, 2025: 471614},
    "Hugh L. Carey Tunnel": {2024: 378955, 2025: 361692},
}

labels = list(data.keys())
vals_2024 = [data[k][2024] for k in labels]
vals_2025 = [data[k][2025] for k in labels]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, vals_2024, width, label='2024')
bars2 = ax.bar(x + width/2, vals_2025, width, label='2025')

for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{int(bar.get_height()):,}', ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Total Vehicles (Jan 5-11)')
ax.set_title('Queens Midtown Tunnel vs Hugh L. Carey Tunnel: 2024 vs 2025')
ax.legend()

plt.savefig('outputs/qmt_hct_yearly.png')
print("Chart saved to outputs/qmt_hct_yearly.png")