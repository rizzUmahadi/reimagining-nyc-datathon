import requests

URL = "https://data.ny.gov/resource/qzve-kjga.json"

for year, (start, end) in [(2024, ("2024-08-05", "2024-08-11")), (2025, ("2025-08-05", "2025-08-11"))]:
    where = (
        f"plaza_id = '27' AND direction = 'I' AND "
        f"date between '{start}T00:00:00' and '{end}T23:59:59'"
    )
    resp = requests.get(URL, params={"$where": where, "$limit": 5})
    print(f"{year}: status {resp.status_code}, rows: {len(resp.json())}")
    print(resp.text[:200])
    print()