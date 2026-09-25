import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Panel 1: 2024 -> 2025 (PS 19 + IS 45)
ax1 = axes[0]
vals1 = [7.48, 7.45]
bars1 = ax1.bar(['2024', '2025'], vals1, color='tab:blue')
for bar, val in zip(bars1, vals1):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:.2f}', ha='center', va='bottom')
ax1.set_ylabel('PM2.5 (µg/m³)')
ax1.set_title('2024 vs 2025\n(matched: PS 19, IS 45)')

# Panel 2: 2025 -> 2026 (Division St, PS 19, CCNY)
ax2 = axes[1]
vals2 = [8.70, 9.36]
bars2 = ax2.bar(['2025', '2026'], vals2, color='tab:orange')
for bar, val in zip(bars2, vals2):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:.2f}', ha='center', va='bottom')
ax2.set_title('2025 vs 2026\n(matched: Division St, PS 19, CCNY)')

fig.suptitle('Manhattan PM2.5, EPA Monitors (Jan-Jul, matched sites per pair)')
plt.tight_layout()
plt.savefig('outputs/manhattan_pm25_pairwise_chart.png')
print("Chart saved to outputs/manhattan_pm25_pairwise_chart.png")