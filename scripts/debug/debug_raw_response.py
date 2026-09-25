import requests

LINK_IDS = [4329472, 4329507, 4329508, 4456511, 4329473]
link_filter = " OR ".join([f"link_id = {lid}" for lid in LINK_IDS])

where = (
    f"({link_filter}) AND "
    f"data_as_of between '2024-01-05T00:00:00' and '2024-01-11T23:59:59' AND "
    f"status = '0'"
)

print("=== THIS IS THE EXACT WHERE CLAUSE BEING SENT ===")
print(where)
print("=== END ===")

resp = requests.get("https://data.ny.gov/resource/i4gi-tjb9.json", params={"$where": where, "$limit": 50000})
print("Status code:", resp.status_code)
print(resp.text[:500])