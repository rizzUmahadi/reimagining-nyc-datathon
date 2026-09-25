import requests
import pandas as pd

URL = "https://data.ny.gov/resource/6amx-2pbv.json"

# Check the actual columns and most recent year available
resp = requests.get(URL, params={"$limit": 5})
df = pd.DataFrame(resp.json())
print("Columns:", df.columns.tolist())
print(df)

# Find the actual most recent year in the data
resp2 = requests.get(URL, params={"$select": "max(year) as latest_year"})
print("\nMost recent year available:", resp2.json())

# Check Bronx coverage specifically
resp3 = requests.get(URL, params={"$select": "distinct county", "$where": "county like '%25Bronx%25'", "$limit": 5})
print("\nBronx county matches:", resp3.json())