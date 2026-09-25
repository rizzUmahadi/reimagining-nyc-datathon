import requests

URL = "https://data.ny.gov/resource/rtih-nq26.json"

resp = requests.get(URL, params={"$limit": 3})
print("Sample rows:")
print(resp.json())

resp2 = requests.get(URL, params={"$order": "date DESC", "$limit": 1})
print("\nMost recent date:")
print(resp2.json())