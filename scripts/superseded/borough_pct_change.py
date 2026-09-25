import matplotlib.pyplot as plt

labels = ['Manhattan', 'Bronx']
changes = [-20.70, 18.38]
colors = ['tab:blue' if c < 0 else 'tab:red' for c in changes]

fig, ax = plt.subplots()
bars = ax.bar(labels, changes, color=colors)

for bar, change in zip(bars, changes):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{change:+.2f}%', ha='center',
             va='bottom' if change > 0 else 'top')

ax.axhline(0, color='black', linewidth=0.8)
plt.ylabel('% Change in Avg Traffic per Segment')
plt.title('Traffic Change by Borough: Manhattan vs Bronx (2024-2025)')
plt.savefig('outputs/borough_pct_change.png')