import pandas as pd

def load(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    df['vol'] = pd.to_numeric(df['vol'], errors='coerce')
    return df

m2024 = load('data/total_traffic_count_2024_manhattan.csv')
m2025 = load('data/total_traffic_count_2025_manhattan.csv')

m2024['key'] = list(zip(m2024['segmentid'], m2024['m'], m2024['d'], m2024['hh'], m2024['mm'], m2024['direction']))
m2025['key'] = list(zip(m2025['segmentid'], m2025['m'], m2025['d'], m2025['hh'], m2025['mm'], m2025['direction']))

common_keys = set(m2024['key']) & set(m2025['key'])
print(f"Exact matching readings (segment+date+hour+minute+direction): {len(common_keys)}")

m2024_exact = m2024[m2024['key'].isin(common_keys)]
m2025_exact = m2025[m2025['key'].isin(common_keys)]

print(f"2024 rows: {len(m2024_exact)}")
print(f"2025 rows: {len(m2025_exact)}")

total_2024 = m2024_exact['vol'].sum()
total_2025 = m2025_exact['vol'].sum()
avg_2024 = m2024_exact['vol'].mean()
avg_2025 = m2025_exact['vol'].mean()

print(f"\nTotal: {total_2024:,.0f} -> {total_2025:,.0f} ({(total_2025-total_2024)/total_2024*100:+.2f}%)")
print(f"Average: {avg_2024:.1f} -> {avg_2025:.1f} ({(avg_2025-avg_2024)/avg_2024*100:+.2f}%)")