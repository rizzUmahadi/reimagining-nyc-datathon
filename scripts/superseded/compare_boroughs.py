import pandas as pd

m2024 = pd.read_csv('data/total_traffic_count_2024_manhattan.csv')
m2025 = pd.read_csv('data/total_traffic_count_2025_manhattan.csv')
b2024 = pd.read_csv('data/total_traffic_count_2024_bronx.csv')
b2025 = pd.read_csv('data/total_traffic_count_2025_bronx.csv')

print("Manhattan 2024 total Vol:", m2024['Vol'].sum())
print("Manhattan 2025 total Vol:", m2025['Vol'].sum())
manhattan_change = (m2025['Vol'].sum() - m2024['Vol'].sum()) / m2024['Vol'].sum() * 100
print(f"Manhattan % change: {manhattan_change:.1f}%")

print()
print("Bronx 2024 total Vol:", b2024['Vol'].sum())
print("Bronx 2025 total Vol:", b2025['Vol'].sum())
bronx_change = (b2025['Vol'].sum() - b2024['Vol'].sum()) / b2024['Vol'].sum() * 100
print(f"Bronx % change: {bronx_change:.1f}%")

print()
print("Row counts (sample size check):")
print("Manhattan 2024 rows:", len(m2024))
print("Manhattan 2025 rows:", len(m2025))
print("Bronx 2024 rows:", len(b2024))
print("Bronx 2025 rows:", len(b2025))