import matplotlib.pyplot as plt

labels = [
    "Bronx-Whitestone\n(Feb 2026 vs Feb 2025)",
    "RFK Bridge\n(YTD thru Feb 2026 vs 2025)",
    "RFK Bridge\n(YTD thru Sep 2025 vs 2024)",
]
values = [-3.9, -4.8, -0.2]

fig, ax = plt.subplots(figsize=(9, 6))
colors = ['tab:red' if v < 0 else 'tab:blue' for v in values]
bars = ax.bar(labels, values, color=colors)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{val:+.1f}%', ha='center',
             va='bottom' if val > 0 else 'top')

ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('% Change in Traffic')
ax.set_title('Bronx-Connecting MTA Crossings: Verified Changes\n(from official MTA Board reports — different time bases, see labels)')
plt.tight_layout()
plt.savefig('outputs/bronx_mta_crossings_verified.png')
print("Chart saved to outputs/bronx_mta_crossings_verified.png")