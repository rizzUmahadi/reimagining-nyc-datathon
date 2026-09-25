import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/equity_combined_analysis.csv')

colors = ['tab:red' if b == 'Bronx' else 'tab:gray' for b in df['Borough']]

fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(df['AgeAdjRate'], df['PM25_change_pct'], c=colors, s=60, alpha=0.8)
ax.axhline(0, color='black', linewidth=0.8)

# Label a few key points
for _, row in df.iterrows():
    if row['Geography'] in ['Mott Haven and Melrose (CD1)', 'Throgs Neck and Co-op City (CD10)', 'Central Harlem (CD10)']:
        ax.annotate(row['Geography'], (row['AgeAdjRate'], row['PM25_change_pct']), fontsize=8, xytext=(5,5), textcoords='offset points')

ax.set_xlabel('Asthma ED Visit Rate, 2023 (per 10,000)')
ax.set_ylabel('PM2.5 % Change, 2024 to 2025')
ax.set_title('Asthma Rate vs PM2.5 Change by District\n(red = Bronx)')
plt.tight_layout()
plt.savefig('outputs/equity_scatter.png')
print("Chart saved to outputs/equity_scatter.png")