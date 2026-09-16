"""
First draft map: combines traffic volume change (early vs recent week),
PM2.5 2024 snapshot by community district, and known CRZ crossing points.
"""

import io
import requests
import pandas as pd
import geopandas as gpd
import folium

# ---------------------------------------------------------------------------
# 1. TRAFFIC: calculate % change by crossing between early and recent week
# ---------------------------------------------------------------------------
early = pd.read_csv("data/traffic_early_week.csv")
recent = pd.read_csv("data/traffic_recent_week.csv")

early_sum = early.groupby("detection_group")["crz_entries"].sum().reset_index()
recent_sum = recent.groupby("detection_group")["crz_entries"].sum().reset_index()

change = early_sum.merge(recent_sum, on="detection_group", suffixes=("_early", "_recent"))
change["pct_change"] = (
    (change["crz_entries_recent"] - change["crz_entries_early"])
    / change["crz_entries_early"] * 100
)

print("=== Traffic % change by crossing ===")
print(change[["detection_group", "pct_change"]].sort_values("pct_change"))

CROSSING_COORDS = {
    "Brooklyn Bridge": (40.7061, -73.9969),
    "Manhattan Bridge": (40.7075, -73.9903),
    "Williamsburg Bridge": (40.7132, -73.9724),
    "Hugh L. Carey Tunnel": (40.7007, -74.0131),
    "Queensboro Bridge": (40.7570, -73.9542),
    "Queens Midtown Tunnel": (40.7440, -73.9660),
    "Lincoln Tunnel": (40.7570, -74.0090),
    "Holland Tunnel": (40.7274, -74.0113),
    "East 60th St": (40.7620, -73.9640),
    "West 60th St": (40.7700, -73.9850),
    "West Side Highway at 60th St": (40.7715, -73.9910),
    "FDR Drive at 60th St": (40.7610, -73.9580),
}

# ---------------------------------------------------------------------------
# 2. AIR QUALITY: load PM2.5 2024, filter to Mean measure
# ---------------------------------------------------------------------------
pm25 = pd.read_csv("data/pm25_2024.csv")
pm25 = pm25[pm25["measure"] == "Annual mean"].copy()
pm25["geo_join_id"] = pm25["geo_join_id"].astype(str).str.zfill(3)

# ---------------------------------------------------------------------------
# 3. BOUNDARIES: download via requests first (fixes the SSL cert issue),
#    then load into geopandas from memory
# ---------------------------------------------------------------------------
BOUNDARY_URL = "https://data.cityofnewyork.us/resource/5crt-au7u.geojson?$limit=100"
resp = requests.get(BOUNDARY_URL)
resp.raise_for_status()
districts = gpd.read_file(io.BytesIO(resp.content))

print("\n=== Boundary file columns (check for the join key) ===")
print(districts.columns.tolist())

JOIN_COL = "boro_cd"  # <-- change this if the printed columns show something else
districts[JOIN_COL] = districts[JOIN_COL].astype(str).str.zfill(3)

districts = districts.merge(pm25, left_on=JOIN_COL, right_on="geo_join_id", how="left")

# ---------------------------------------------------------------------------
# 4. BUILD THE MAP
# ---------------------------------------------------------------------------
m = folium.Map(location=[40.75, -73.97], zoom_start=11, tiles="OpenStreetMap")

folium.Choropleth(
    geo_data=districts,
    data=districts,
    columns=[JOIN_COL, "data_value"],
    key_on=f"feature.properties.{JOIN_COL}",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="PM2.5 (µg/m³), 2024 Annual Average",
    name="Air Quality (2024)",
).add_to(m)

for _, row in change.iterrows():
    coords = CROSSING_COORDS.get(row["detection_group"])
    if coords is None:
        continue
    color = "red" if row["pct_change"] > 0 else "blue"
    folium.CircleMarker(
        location=coords,
        radius=min(abs(row["pct_change"]), 20) + 5,
        popup=f"{row['detection_group']}: {row['pct_change']:.1f}% change",
        tooltip=row["detection_group"],
        color=color,
        fill=True,
        fill_opacity=0.7,
    ).add_to(m)

folium.LayerControl().add_to(m)
m.save("outputs/draft_map.html")
print("\nMap saved to outputs/draft_map.html — open it in your browser to view.")

# Debug: compare the actual join key values on both sides
print("\n=== boro_cd sample values ===")
print(districts["boro_cd"].unique()[:10] if "boro_cd" in districts.columns else "boro_cd column missing after merge")
print("\n=== geo_join_id sample values ===")
print(pm25["geo_join_id"].unique()[:10])
