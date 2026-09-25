import requests

URL = "https://data.ny.gov/resource/aq4q-6svx.json"

resp = requests.get(URL, params={"$order": "date DESC", "$limit": 3})
print("Most recent data:")
print(resp.json())

resp2 = requests.get(URL, params={"$select": "distinct facility"})
print("\nFacilities covered:")
print(resp2.json())