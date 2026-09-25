import requests

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

url = "https://aqs.epa.gov/data/api/dailyData/byCounty"

for label, bdate, edate in [
    ("Feb 2026", "20260201", "20260228"),
    ("Mar 2026", "20260301", "20260331"),
    ("Apr 2026", "20260401", "20260430"),
    ("May 2026", "20260501", "20260531"),
    ("Jun 2026", "20260601", "20260630"),
    ("Jul 2026", "20260701", "20260731"),
]:
    params = {
        "email": EMAIL, "key": KEY,
        "param": "88101",
        "state": "36", "county": "005",
        "bdate": bdate, "edate": edate,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    print(f"{label}: rows={len(data.get('Data', []))}")