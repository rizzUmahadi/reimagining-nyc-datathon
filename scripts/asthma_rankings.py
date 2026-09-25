import pandas as pd

df = pd.read_csv('data/asthma_ed_visits_adults_2023.csv')

print("Geography levels in this file:")
print(df['GeoTypeDesc'].value_counts())

cd_only = df[df['GeoTypeDesc'] == 'Community District'].copy()
print(f"\nFiltered to Community District: {len(cd_only)} rows")

# Clean the Number column (has commas) and rate columns
cd_only['Number'] = cd_only['Number'].str.replace(',', '').astype(int)
cd_only['Age-adjusted rate per 10,000'] = pd.to_numeric(cd_only['Age-adjusted rate per 10,000'], errors='coerce')

ranked = cd_only.sort_values('Age-adjusted rate per 10,000', ascending=False)

print("\n=== TOP 10 districts by asthma ED visit rate ===")
print(ranked[['Geography', 'Borough', 'Age-adjusted rate per 10,000']].head(10).to_string(index=False))

print("\n=== BOTTOM 10 districts (lowest rate) ===")
print(ranked[['Geography', 'Borough', 'Age-adjusted rate per 10,000']].tail(10).to_string(index=False))