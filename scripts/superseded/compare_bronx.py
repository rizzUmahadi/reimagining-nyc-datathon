import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

b2024 = pd.read_csv('data/total_traffic_count_2024_bronx.csv')
b2025 = pd.read_csv('data/total_traffic_count_2025_bronx.csv')

b2024['Vol'] = pd.to_numeric(b2024['Vol'], errors='coerce')
b2025['vol'] = pd.to_numeric(b2025['vol'], errors='coerce')

labels = ['2024', '2025']
totals = [b2024['Vol'].sum(), b2025['vol'].sum()]

print("2024 total:", totals[0])
print("2025 total:", totals[1])

change = (totals[1] - totals[0]) / totals[0] * 100
print(f"Percent change: {change:.2f}%")

fig, ax = plt.subplots()
bars = ax.bar(labels, totals)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

for bar, total in zip(bars, totals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{int(total):,}', ha='center', va='bottom')

plt.ylabel('Total Vehicle Volume')
plt.title('Bronx Traffic: 2024 vs 2025')
plt.savefig('outputs/bronx_comparison.png')