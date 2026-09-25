import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import io

GEOFENCE_URL = "https://data.ny.gov/resource/srxy-5nxn.geojson"
resp = requests.get(GEOFENCE_URL)
resp.raise_for_status()
crz_boundary = gpd.read_file(io.BytesIO(resp.content))

print("Geofence loaded:", len(crz_boundary), "polygon(s)")
print(crz_boundary.columns.tolist())

sensors = pd.read_csv('data/manhattan_sensor_points.csv')

sensors['geometry'] = sensors.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
sensors_gdf = gpd.GeoDataFrame(sensors, geometry='geometry', crs=crz_boundary.crs)

inside = gpd.sjoin(sensors_gdf, crz_boundary, predicate='within', how='inner')

print(f"\nSensors inside the CRZ: {len(inside)} out of {len(sensors)}")
print(inside[['link_id', 'link_name', 'lat', 'lon']].to_string())