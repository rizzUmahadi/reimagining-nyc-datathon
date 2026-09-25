import requests

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

# 88101 is the official EPA parameter code for PM2.5 (FRM/FEM - the regulatory standard)
url = "https://aqs.epa.gov/data/api/list/sitesByCounty"
params = {"email": EMAIL, "key": KEY, "state": "36", "county": "005"}  # Bronx

resp = requests.get(url, params=params)
data = resp.json()

print(f"Total sites in Bronx: {len(data.get('Data', []))}")
for row in data.get('Data', []):
    print(row)