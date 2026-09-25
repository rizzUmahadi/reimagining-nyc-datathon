import requests
import pandas as pd

BNT_URL = "https://data.ny.gov/resource/qzve-kjga.json"
CRZ_URL = "https://data.ny.gov/resource/t6yz-b64h.json"

print("=== 2024 — ALL distinct dates ===")
where_2024 = "plaza_id = '28' AND direction = 'I' AND date between '2024-01-05T00:00:00' and '2024-01-11T23:59:59'"
resp = requests.get(BNT_URL, params={"$select": "distinct date", "$where": where_2024, "$limit": 50})
df = pd.DataFrame(resp.json())
print(sorted(df['date'].unique()) if not df.empty else "NO DATA")

print("\n=== 2025 — ALL distinct dates ===")
where_2025 = "plaza_id = '28' AND direction = 'I' AND date between '2025-01-05T00:00:00' and '2025-01-11T23:59:59'"
resp = requests.get(BNT_URL, params={"$select": "distinct date", "$where": where_2025, "$limit": 50})
df = pd.DataFrame(resp.json())
print(sorted(df['date'].unique()) if not df.empty else "NO DATA")

print("\n=== 2026 — ALL distinct dates ===")
where_2026 = "detection_group = 'Hugh L. Carey Tunnel' AND toll_date between '2026-01-05T00:00:00' and '2026-01-11T23:59:59'"
resp = requests.get(CRZ_URL, params={"$select": "distinct toll_date", "$where": where_2026, "$limit": 50})
df = pd.DataFrame(resp.json())
print(sorted(df['toll_date'].unique()) if not df.empty else "NO DATA")