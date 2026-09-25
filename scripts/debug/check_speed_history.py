import requests

URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"

for label, date_str in [("Jan 2024", "2024-01-15"), ("Jan 2025", "2025-01-15"), ("Jun 2025", "2025-06-15")]:
    resp = requests.get(URL, params={
        "$where": f"data_as_of between '{date_str}T00:00:00' and '{date_str}T23:59:59'",
        "$limit": 5,
    })
    rows = resp.json()
    print(f"{label}: {len(rows)} rows found")