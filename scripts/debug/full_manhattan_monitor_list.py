import requests

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

url = "https://aqs.epa.gov/data/api/monitors/byCounty"
params = {
    "email": EMAIL, "key": KEY,
    "param": "88101",
    "state": "36", "county": "061",
    "bdate": "20200101", "edate": "20261231",
}

resp = requests.get(url, params=params)
data = resp.json()

seen = set()
for row in data.get('Data', []):
    site = row.get('site_number')
    name = row.get('local_site_name')
    open_date = row.get('open_date')
    close_date = row.get('close_date')
    key = (site, name)
    if key not in seen:
        seen.add(key)
        print(f"{site} - {name} | open: {open_date} | close: {close_date}")