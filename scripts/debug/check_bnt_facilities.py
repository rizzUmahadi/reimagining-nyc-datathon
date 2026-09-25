import requests
import pandas as pd

URL = "https://data.ny.gov/resource/qzve-kjga.json"

resp = requests.get(URL, params={"$limit": 5})
df = pd.DataFrame(resp.json())
print(df.columns.tolist())
print(df)