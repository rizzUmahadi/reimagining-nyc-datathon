import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"

# Just pull 20 sample rows to see the real column names before building anything
resp = requests.get(URL, params={"$limit": 20})
df = pd.DataFrame(resp.json())
print(df.columns.tolist())
print(df.head())