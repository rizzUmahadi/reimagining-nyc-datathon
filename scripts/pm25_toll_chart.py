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

# Districts tied directly to the crossings analyzed in this project:
# - All Manhattan (the toll zone itself)
# - Mott Haven/Melrose (CD1) & Hunts Point/Longwood (CD2) - near RFK Bridge Bronx side
# - Throgs Neck and Co-op City (CD10) - near Throgs Neck & Bronx-Whitestone Bridges
# - Long Island City and Astoria (Queens CD1) - near Queens Midtown Tunnel Queens side
relevant_geoids = [
    '101','102','103','104','105','106','107','108','109','110','111','112',  # all Manhattan
    '201','202','210',  # Bronx: Mott Haven, Hunts Point, Throgs Neck/Co-op City
    '401',  # Queens: LIC/Astoria
]

toll_related = merged[merged['GeoID'].astype(str).isin(relevant_geoids)].sort_values('change_pct')

colors = ['tab:red' if v > 0 else 'tab:blue' for v in toll_related['change_pct']]

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(toll_related['Geography'], toll_related['change_pct'], color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('% Change in PM2.5, 2024 to 2025')
ax.set_title('PM2.5 Change: Districts Directly Tied to Toll Crossings\n(Manhattan CRZ + Bronx/Queens crossing-adjacent districts)')
plt.tight_layout()
plt.savefig('outputs/pm25_toll_related.png')
print("Chart saved to outputs/pm25_toll_related.png")

print(toll_related[['Geography', 'Borough', 'change_pct']].to_string(index=False))