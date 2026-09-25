import pandas as pd

df = pd.read_csv('data/asthma_ed_visits_adults_2023.csv')
cd_only = df[df['GeoTypeDesc'] == 'Community District'].copy()
cd_only['Number'] = cd_only['Number'].str.replace(',', '').astype(int)
cd_only['Age-adjusted rate per 10,000'] = pd.to_numeric(cd_only['Age-adjusted rate per 10,000'], errors='coerce')

# Check 1: exactly 59 rows, no duplicates
print(f"Row count: {len(cd_only)} (should be 59)")
print(f"Duplicate GeoIDs: {cd_only['GeoID'].duplicated().sum()} (should be 0)")

# Check 2: any missing/blank rate values?
print(f"Missing rate values: {cd_only['Age-adjusted rate per 10,000'].isna().sum()} (should be 0)")

# Check 3: do the 59 district totals roughly add up to the citywide total?
citywide_row = df[df['GeoTypeDesc'] == 'Citywide']
citywide_total = int(citywide_row['Number'].values[0].replace(',', ''))
district_sum = cd_only['Number'].sum()
print(f"\nCitywide total (reported): {citywide_total:,}")
print(f"Sum of all 59 districts: {district_sum:,}")
print(f"Difference: {citywide_total - district_sum:,} ({(citywide_total - district_sum) / citywide_total * 100:.1f}%)")