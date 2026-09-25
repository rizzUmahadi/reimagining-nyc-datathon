import pandas as pd

b2024 = pd.read_csv('data/bronx_speed_2024.csv')
print(b2024['status'].unique())
print(b2024['status'].dtype)