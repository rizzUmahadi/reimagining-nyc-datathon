import pandas as pd

df = pd.read_csv('data/manhattan_pm25_epa_2024_2025_2026.csv')

sites_2024 = set(df[df['Year'] == 2024]['local_site_name'])
sites_2025 = set(df[df['Year'] == 2025]['local_site_name'])
sites_2026 = set(df[df['Year'] == 2026]['local_site_name'])

print("2024 sites:", sites_2024)
print("2025 sites:", sites_2025)
print("2026 sites:", sites_2026)

print("\nSites common to 2024 AND 2025:", sites_2024 & sites_2025)
print("Sites common to 2025 AND 2026:", sites_2025 & sites_2026)
print("Sites common to ALL THREE:", sites_2024 & sites_2025 & sites_2026)

# Pairwise comparison using only matched sites
for label, y1, y2, common in [
    ("2024 -> 2025", 2024, 2025, sites_2024 & sites_2025),
    ("2025 -> 2026", 2025, 2026, sites_2025 & sites_2026),
]:
    sub1 = df[(df['Year'] == y1) & (df['local_site_name'].isin(common))]
    sub2 = df[(df['Year'] == y2) & (df['local_site_name'].isin(common))]
    avg1 = sub1['arithmetic_mean'].mean()
    avg2 = sub2['arithmetic_mean'].mean()
    change = (avg2 - avg1) / avg1 * 100
    print(f"\n{label} (matched sites: {common}): {avg1:.2f} -> {avg2:.2f} ({change:+.2f}%)")