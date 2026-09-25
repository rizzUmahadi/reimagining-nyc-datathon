import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data/lincoln_holland_monthly.csv')

# Verify only rows that actually have numbers (skip blank 2026 rows)
has_data = df['total_vehicles'].notna()
df.loc[has_data, 'calculated_total'] = df.loc[has_data, 'automobiles'] + df.loc[has_data, 'buses'] + df.loc[has_data, 'trucks']
mismatch = has_data & (df['calculated_total'] != df['total_vehicles'])

if mismatch.any():
    print("WARNING: Found rows where the numbers don't add up:")
    print(df[mismatch])
else:
    print("Verified: every available row's Automobiles + Buses + Trucks = Total Vehicles. Data is clean.")

month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

for crossing in ['Lincoln Tunnel', 'Holland Tunnel']:
    print(f"\n=== {crossing} ===")
    sub = df[df['crossing'] == crossing]

    for month in range(1, 13):
        month_data = sub[sub['month'] == month].set_index('year')['total_vehicles']
        v2024, v2025, v2026 = month_data[2024], month_data[2025], month_data[2026]

        change_25 = (v2025 - v2024) / v2024 * 100
        v2026_str = f"{v2026:,.0f}" if pd.notna(v2026) else "N/A"
        change_26_str = f"({(v2026 - v2025) / v2025 * 100:+.2f}%)" if pd.notna(v2026) else ""

        print(f"{month_names[month]}: {v2024:,.0f} -> {v2025:,.0f} ({change_25:+.2f}%) -> {v2026_str} {change_26_str}")

    fig, ax = plt.subplots()
    for year in [2024, 2025, 2026]:
        yearly = sub[sub['year'] == year].sort_values('month')
        ax.plot(yearly['month'], yearly['total_vehicles'], marker='o', label=str(year))
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([month_names[m] for m in range(1, 13)])
    ax.set_ylabel('Total Vehicles')
    ax.set_title(f'{crossing}: Monthly Traffic, Full Year 2024 vs 2025 vs 2026 (partial)')
    ax.legend()
    filename = crossing.lower().replace(' ', '_')
    plt.savefig(f'outputs/{filename}_monthly.png')
    print(f"Chart saved to outputs/{filename}_monthly.png")