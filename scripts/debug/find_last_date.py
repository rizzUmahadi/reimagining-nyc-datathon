import requests

URL = "https://data.ny.gov/resource/qzve-kjga.json"

resp = requests.get(URL, params={"$order": "date DESC", "$limit": 1})
print(resp.json())