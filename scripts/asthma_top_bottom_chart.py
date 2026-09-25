import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/asthma_ed_visits_adults_2023.csv')
cd_only = df[df['GeoTypeDesc'] == 'Community District'].copy()
cd_only['Number'] = cd_only['Number'].str.replace(',', '').astype(int)
cd_only['Age-adjusted rate per 10,000'] = pd.to_numeric(cd_only['Age-adjusted rate per 10,000'], errors='coerce')

ranked = cd_only.sort_values('Age-adjusted rate per 10,000', ascending=False)

top15 = ranked.head(15)
bottom15 = ranked.tail(15)
combined = pd.concat([top15, bottom15]).sort_values('Age-adjusted rate per 10,000', ascending=True)

colors = ['tab:red' if b == 'Bronx' else 'tab:blue' for b in combined['Borough']]

fig, ax = plt.subplots(figsize=(10, 10))
ax.barh(combined['Geography'], combined['Age-adjusted rate per 10,000'], color=colors)
ax.set_xlabel('Age-Adjusted Asthma ED Visit Rate (per 10,000)')
ax.set_title('Asthma ED Visit Rates: Top 15 & Bottom 15 Districts, 2023\n(Bronx districts in red)')
plt.tight_layout()
plt.savefig('outputs/asthma_top_bottom.png')
print("Chart saved to outputs/asthma_top_bottom.png")