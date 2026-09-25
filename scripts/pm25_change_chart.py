import pandas as pd
import matplotlib.pyplot as plt

df24 = pd.read_csv('data/pm2.5_2024.csv')
df25 = pd.read_csv('data/pm2.5_2025.csv')

cd24 = df24[df24['GeoTypeDesc'] == 'Community District'].copy()
cd25 = df25[df25['GeoTypeDesc'] == 'Community District'].copy()

merged = cd24[['GeoID', 'Geography', 'Borough', 'Annual mean mcg/m3']].merge(
    cd25[['GeoID', 'Annual mean mcg/m3']], on='GeoID', suffixes=('_2024', '_2025')
)
merged['change_pct'] = (merged['Annual mean mcg/m3_2025'] - merged['Annual mean mcg/m3_2024']) / merged['Annual mean mcg/m3_2024'] * 100

ranked = merged.sort_values('change_pct', ascending=False)
top10 = ranked.head(10)
bottom10 = ranked.tail(10)
combined = pd.concat([top10, bottom10]).sort_values('change_pct')

colors = ['tab:red' if v > 0 else 'tab:blue' for v in combined['change_pct']]

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(combined['Geography'], combined['change_pct'], color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('% Change in PM2.5, 2024 to 2025')
ax.set_title('PM2.5 Change by Community District: 10 Biggest Increases & Decreases\n(red = worse, blue = improved)')
plt.tight_layout()
plt.savefig('outputs/pm25_change_by_district.png')
print("Chart saved to outputs/pm25_change_by_district.png")