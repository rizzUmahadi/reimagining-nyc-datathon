import requests

URL = "https://data.ny.gov/resource/ebfx-2m7v.json"

resp = requests.get(URL, params={"$order": "date ASC", "$limit": 1})
print("Earliest date:", resp.json())

resp2 = requests.get(URL, params={"$select": "distinct facility"})
print("\nAll facilities:")
for f in resp2.json():
    print(" ", f['facility'])