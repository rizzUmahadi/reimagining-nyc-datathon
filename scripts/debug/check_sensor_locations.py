import requests
import pandas as pd

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

resp = requests.get(URL, params={
    "$where": "borough = 'Manhattan'",
    "$limit": 20,
})
df = pd.DataFrame(resp.json())

print(f"Sample Manhattan sensors: {len(df)}")
print(df[['link_id', 'link_name', 'link_points']].to_string())