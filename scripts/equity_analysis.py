import pandas as pd

# Load asthma (2023 baseline)
asthma = pd.read_csv('data/asthma_ed_visits_adults_2023.csv')
asthma_cd = asthma[asthma['GeoTypeDesc'] == 'Community District'].copy()
asthma_cd['GeoID'] = asthma_cd['GeoID'].astype(int)
asthma_cd['AgeAdjRate'] = pd.to_numeric(asthma_cd['Age-adjusted rate per 10,000'], errors='coerce')

# Load verified PM2.5 (2024, 2025)
pm25 = pd.read_csv('data/pm25_official_2024_2025.csv')
pm25_wide = pm25.pivot(index='GeoID', columns='Year', values='Value').reset_index()
pm25_wide.columns = ['GeoID', 'PM25_2024', 'PM25_2025']
pm25_wide['PM25_change_pct'] = (pm25_wide['PM25_2025'] - pm25_wide['PM25_2024']) / pm25_wide['PM25_2024'] * 100

# Merge everything together
combined = asthma_cd[['GeoID', 'Geography', 'Borough', 'AgeAdjRate']].merge(pm25_wide, on='GeoID')

print(f"Merged: {len(combined)} districts (should be 59)")

# Real question: do high-asthma districts show worsening PM2.5, or improving?
high_asthma = combined.sort_values('AgeAdjRate', ascending=False).head(15)
print("\n=== TOP 15 HIGHEST-ASTHMA DISTRICTS: their PM2.5 change ===")
print(high_asthma[['Geography', 'Borough', 'AgeAdjRate', 'PM25_change_pct']].to_string(index=False))

low_asthma = combined.sort_values('AgeAdjRate', ascending=False).tail(15)
print("\n=== 15 LOWEST-ASTHMA DISTRICTS: their PM2.5 change ===")
print(low_asthma[['Geography', 'Borough', 'AgeAdjRate', 'PM25_change_pct']].to_string(index=False))

# Overall correlation
corr = combined['AgeAdjRate'].corr(combined['PM25_change_pct'])
print(f"\nCorrelation between asthma rate and PM2.5 change: {corr:.3f}")

combined.to_csv('data/equity_combined_analysis.csv', index=False)
print("\nSaved full combined dataset to data/equity_combined_analysis.csv")