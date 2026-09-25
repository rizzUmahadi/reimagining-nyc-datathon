import requests

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

print("=== TEST: link_id as quoted string ===")
resp = requests.get(URL, params={"$where": "link_id = '4329472'", "$limit": 5})
print("Status:", resp.status_code, "-", resp.text[:200])
# Test 2: ONLY the status filter, nothing else
print("\n=== TEST 2: status only (unquoted) ===")
resp = requests.get(URL, params={"$where": "status = 0", "$limit": 5})
print("Status:", resp.status_code, "-", resp.text[:200])

# Test 3: status as quoted string
print("\n=== TEST 3: status only (quoted) ===")
resp = requests.get(URL, params={"$where": "status = '0'", "$limit": 5})
print("Status:", resp.status_code, "-", resp.text[:200])