import pandas as pd
import matplotlib.pyplot as plt

pm25 = pd.read_csv('data/pm25_official_2024_2025.csv')
names = pd.read_csv('data/pm25_2024.csv')
names_cd = names[(names['geo_type_name'] == 'CD') & (names['name'] == 'Fine particles (PM 2.5)') & (names['measure'] == 'Annual average')][['geo_join_id', 'geo_place_name']].copy()
names_cd.columns = ['GeoID', 'Geography']
names_cd['GeoID'] = names_cd['GeoID'].astype(str).str.zfill(3)
names_cd = names_cd.drop_duplicates(subset='GeoID')

wide = pm25.pivot(index='GeoID', columns='Year', values='Value').reset_index()
wide.columns = ['GeoID', 'PM25_2024', 'PM25_2025']
wide['GeoID'] = wide['GeoID'].astype(str).str.zfill(3)
wide = wide.merge(names_cd, on='GeoID')
wide['change'] = wide['PM25_2025'] - wide['PM25_2024']

print(f"Row count (should be 59): {len(wide)}")

borough_map = {'1': 'Manhattan', '2': 'Bronx', '3': 'Brooklyn', '4': 'Queens', '5': 'Staten Island'}
wide['Borough'] = wide['GeoID'].str[0].map(borough_map)
wide = wide[wide['Borough'] != 'Staten Island'].copy()

borough_order = ['Queens', 'Bronx', 'Brooklyn', 'Manhattan']
wide['borough_rank'] = wide['Borough'].map({b: i for i, b in enumerate(borough_order)})
wide = wide.sort_values(['borough_rank', 'change'], ascending=[True, False])

colors = {'Queens': 'firebrick', 'Bronx': 'sandybrown', 'Brooklyn': 'lightsteelblue', 'Manhattan': 'steelblue'}
bar_colors = wide['Borough'].map(colors)

fig, ax = plt.subplots(figsize=(12, 16))
ax.barh(wide['Geography'], wide['change'], color=bar_colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Change in Annual Mean PM2.5 (mcg/m3)')
ax.set_title('PM2.5 Change (2024 to 2025) Grouped by Borough (Excluding Staten Island)', fontsize=14)

net_change = wide.groupby('Borough')['change'].mean().round(3)
box_text = "Borough Net Change (mcg/m3):\n" + "\n".join([f"{b:12s}: {net_change[b]:+.3f}" for b in borough_order])
ax.text(0.98, 0.97, box_text, transform=ax.transAxes, fontsize=10, verticalalignment='top',
        horizontalalignment='right', family='monospace',
        bbox=dict(boxstyle='round', facecolor='mistyrose', edgecolor='gray'))

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('outputs/pm25_borough_change_CORRECTED.png', dpi=150)
print("Saved outputs/pm25_borough_change_CORRECTED.png")

print("\nThrogs Neck check:")
print(wide[wide['Geography'].str.contains('Throgs Neck')][['Geography', 'Borough', 'PM25_2024', 'PM25_2025', 'change']])