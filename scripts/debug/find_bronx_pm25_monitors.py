import requests

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

# 88101 = PM2.5 (regulatory standard parameter code)
url = "https://aqs.epa.gov/data/api/monitors/byCounty"
params = {
    "email": EMAIL, "key": KEY,
    "param": "88101",
    "state": "36", "county": "005",
    "bdate": "20260101", "edate": "20260930",
}

resp = requests.get(url, params=params)
data = resp.json()

print(f"PM2.5 monitors active in Bronx in 2026: {len(data.get('Data', []))}")
for row in data.get('Data', []):
    print(row.get('site_number'), '-', row.get('local_site_name'), '| active:', row.get('open_date'), 'to', row.get('close_date'))