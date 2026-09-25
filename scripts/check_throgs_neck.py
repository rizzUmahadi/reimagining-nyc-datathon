import pandas as pd
pm25 = pd.read_csv('data/pm25_official_2024_2025.csv')
print(pm25[pm25['GeoID'] == 210])