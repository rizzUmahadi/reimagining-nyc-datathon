import pandas as pd

df24 = pd.read_csv('data/pm2.5_2024.csv')
df25 = pd.read_csv('data/pm2.5_2025.csv')

cd24 = df24[df24['GeoTypeDesc'] == 'Community District'].copy()
cd25 = df25[df25['GeoTypeDesc'] == 'Community District'].copy()

print(f"2024 CD rows: {len(cd24)}, 2025 CD rows: {len(cd25)}")

merged = cd24[['GeoID', 'Geography', 'Annual mean mcg/m3']].merge(
    cd25[['GeoID', 'Annual mean mcg/m3']], on='GeoID', suffixes=('_2024', '_2025')
)
merged['change_pct'] = (merged['Annual mean mcg/m3_2025'] - merged['Annual mean mcg/m3_2024']) / merged['Annual mean mcg/m3_2024'] * 100

print("\n=== BIGGEST INCREASE, 2024->2025 ===")
print(merged.sort_values('change_pct', ascending=False).head(10).to_string(index=False))

print("\n=== BIGGEST DECREASE ===")
print(merged.sort_values('change_pct').head(10).to_string(index=False))