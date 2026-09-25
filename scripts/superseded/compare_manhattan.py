import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

m2024 = pd.read_csv('data/total_traffic_count_2024_manhattan.csv')
m2025 = pd.read_csv('data/total_traffic_count_2025_manhattan.csv')

m2024['Vol'] = pd.to_numeric(m2024['Vol'], errors='coerce')
m2025['Vol'] = pd.to_numeric(m2025['Vol'], errors='coerce')

labels = ['2024', '2025']
totals = [m2024['Vol'].sum(), m2025['Vol'].sum()]

print("2024 total:", totals[0])
print("2025 total:", totals[1])

fig, ax = plt.subplots()
bars = ax.bar(labels, totals)

# turn off the confusing 1e6 shorthand, show full numbers with commas instead
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

# print the actual number on top of each bar
for bar, total in zip(bars, totals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{int(total):,}', ha='center', va='bottom')

plt.ylabel('Total Vehicle Volume')
plt.title('Manhattan Traffic: 2024 vs 2025')
plt.savefig('outputs/manhattan_comparison.png')