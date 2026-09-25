import requests
import pandas as pd

URL = "https://data.ny.gov/resource/qzve-kjga.json"

resp = requests.get(URL, params={"$select": "distinct plaza_id", "$limit": 50})
df = pd.DataFrame(resp.json())
print(df)