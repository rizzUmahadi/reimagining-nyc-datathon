import requests
import pandas as pd

URL = "https://data.ny.gov/resource/ebfx-2m7v.json"

resp = requests.get(URL, params={"$limit": 5})
print("Status:", resp.status_code)
print(resp.json())

# If it works, check the real date range
resp2 = requests.get(URL, params={"$order": "date DESC", "$limit": 1})
print("\nMost recent (if 'date' column exists):", resp2.json())