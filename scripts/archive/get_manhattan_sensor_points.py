import requests
import pandas as pd

URL = "https://data.ny.gov/resource/i4gi-tjb9.json"

resp = requests.get(URL, params={
    "$select": "distinct link_id, link_name, link_points",
    "$where": "borough = 'Manhattan' AND data_as_of between '2026-09-01T00:00:00' and '2026-09-01T23:59:59'",
    "$limit": 500,
})
df = pd.DataFrame(resp.json())

def first_point(points_str):
    first_pair = points_str.split(" ")[0]
    lat, lon = first_pair.split(",")
    return float(lat), float(lon)

df[['lat', 'lon']] = df['link_points'].apply(lambda p: pd.Series(first_point(p)))

print(f"Total distinct Manhattan sensors: {len(df)}")
print(df[['link_id', 'link_name', 'lat', 'lon']].to_string())
df[['link_id', 'link_name', 'lat', 'lon']].to_csv('data/manhattan_sensor_points.csv', index=False)