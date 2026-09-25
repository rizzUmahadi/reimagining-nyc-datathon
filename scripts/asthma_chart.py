import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/asthma_ed_visits_adults_2023.csv')
cd_only = df[df['GeoTypeDesc'] == 'Community District'].copy()
cd_only['Number'] = cd_only['Number'].str.replace(',', '').astype(int)
cd_only['Age-adjusted rate per 10,000'] = pd.to_numeric(cd_only['Age-adjusted rate per 10,000'], errors='coerce')

ranked = cd_only.sort_values('Age-adjusted rate per 10,000', ascending=True)

# Color Bronx districts differently to highlight the pattern
colors = ['tab:red' if b == 'Bronx' else 'tab:blue' for b in ranked['Borough']]

fig, ax = plt.subplots(figsize=(10, 14))
ax.barh(ranked['Geography'], ranked['Age-adjusted rate per 10,000'], color=colors)
ax.set_xlabel('Age-Adjusted Asthma ED Visit Rate (per 10,000)')
ax.set_title('Asthma ED Visit Rates by Community District, 2023\n(Bronx districts in red)')
plt.tight_layout()
plt.savefig('outputs/asthma_rates_by_district.png')
print("Chart saved to outputs/asthma_rates_by_district.png")