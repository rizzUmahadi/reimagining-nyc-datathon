import requests
import pandas as pd

URL = "https://data.ny.gov/resource/6amx-2pbv.json"

resp = requests.get(URL, params={"$select": "max(aadt_year) as latest_year"})
print("Most recent AADT year available:", resp.json())

resp2 = requests.get(URL, params={"$select": "distinct aadt_year", "$where": "county = 'Bronx'"})
df = pd.DataFrame(resp2.json())
print("\nAll years with Bronx data:")
print(sorted(df['aadt_year'].astype(int).unique()))