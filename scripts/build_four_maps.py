import io
import requests
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

BOUNDARY_URL = "https://data.cityofnewyork.us/resource/5crt-au7u.geojson?$limit=100"
resp = requests.get(BOUNDARY_URL)
districts = gpd.read_file(io.BytesIO(resp.content))
districts['boro_cd'] = districts['boro_cd'].astype(str).str.zfill(3)

pm25 = pd.read_csv('data/pm25_official_2024_2025.csv')
names = pd.read_csv('data/pm25_2024.csv')
names_cd = names[names['geo_type_name'] == 'CD'][['geo_join_id', 'geo_place_name']].copy()
names_cd.columns = ['GeoID', 'Geography']
names_cd['GeoID'] = names_cd['GeoID'].astype(str).str.zfill(3)
names_cd = names_cd.drop_duplicates(subset='GeoID')

vmin = pm25['Value'].min()
vmax = pm25['Value'].max()
colormap = cm.LinearColormap(colors=['green', 'yellow', 'orange', 'red'], vmin=vmin, vmax=vmax,
                              caption='PM2.5 (ug/m3)')

NYC_BOUNDS = [[40.53, -74.18], [40.90, -73.72]]

def build_district_map(year, filename):
    yr_data = pm25[pm25['Year'] == year][['GeoID', 'Value']].copy()
    yr_data['GeoID'] = yr_data['GeoID'].astype(str).str.zfill(3)
    yr_data = yr_data.merge(names_cd, on='GeoID')

    d = districts.merge(yr_data, left_on='boro_cd', right_on='GeoID', how='left')

    m = folium.Map(tiles="OpenStreetMap")
    m.fit_bounds(NYC_BOUNDS)

    def style_fn(feature):
        val = feature['properties'].get('Value')
        if val is None:
            return {'fillColor': '#cccccc', 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.3}
        return {'fillColor': colormap(val), 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.85}

    folium.GeoJson(
        d, style_function=style_fn,
        tooltip=folium.GeoJsonTooltip(fields=['Geography', 'Value'], aliases=['District:', 'PM2.5:'], localize=True)
    ).add_to(m)
    colormap.add_to(m)

    top3 = yr_data.nlargest(3, 'Value')
    bottom3 = yr_data.nsmallest(3, 'Value')
    labeled = pd.concat([top3, bottom3])

    for _, row in labeled.iterrows():
        geo = d[d['GeoID'] == row['GeoID']]
        if geo.empty:
            continue
        pt = geo.geometry.centroid.iloc[0]
        folium.Marker(
            location=[pt.y, pt.x],
            icon=folium.DivIcon(html=f'''<div style="font-size: 11px; font-weight: bold; color: black;
                background: white; padding: 2px 5px; border-radius: 3px; border: 1px solid #333;
                white-space: nowrap;">{row['Geography']}<br>{row['Value']:.1f}</div>''')
        ).add_to(m)

    title_html = f'''<div style="position: fixed; top: 10px; left: 50px; z-index: 9999;
        background: white; padding: 10px 20px; border-radius: 5px; font-size: 20px; font-weight: bold;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">PM2.5 by NYC Community District - {year}</div>'''
    m.get_root().html.add_child(folium.Element(title_html))

    m.save(f'outputs/{filename}')
    print(f"Saved {filename}")

build_district_map(2024, 'map_2024_v2.html')
build_district_map(2025, 'map_2025_v2.html')

bronx_sites = {'IS 52': (40.8615, -73.8790), 'IS 74': (40.8443, -73.8380), 'PFIZER LAB SITE': (40.8087, -73.9160)}
manhattan_sites = {'PS 19': (40.7180, -73.9760), 'IS 45': (40.8100, -73.9450), 'CCNY': (40.8200, -73.9500), 'DIVISION STREET': (40.7140, -73.9950)}

bronx_epa = pd.read_csv('data/bronx_pm25_epa_2024_2025_2026.csv')
manhattan_epa = pd.read_csv('data/manhattan_pm25_epa_2024_2025_2026.csv')

m3 = folium.Map(tiles="OpenStreetMap")
m3.fit_bounds(NYC_BOUNDS)

for site, coords in {**bronx_sites, **manhattan_sites}.items():
    df = bronx_epa if site in bronx_sites else manhattan_epa
    vals = df[(df['local_site_name'] == site) & (df['Year'] == 2026)]['arithmetic_mean']
    if vals.empty:
        continue
    avg = vals.mean()
    folium.CircleMarker(location=coords, radius=18, color='darkred', fill=True, fill_color='red', fill_opacity=0.8,
                         weight=2).add_to(m3)
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(html=f'''<div style="font-size: 13px; font-weight: bold; color: black;
            background: white; padding: 2px 6px; border-radius: 4px; border: 1px solid #333;
            transform: translate(20px, -10px); white-space: nowrap;">{site}: {avg:.1f} ug/m3</div>''')
    ).add_to(m3)

title_html3 = '''<div style="position: fixed; top: 10px; left: 50px; z-index: 9999;
    background: white; padding: 10px 20px; border-radius: 5px; font-size: 20px; font-weight: bold;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">PM2.5 - Real EPA Monitors, 2026 (Jan-Jul, partial year)</div>'''
m3.get_root().html.add_child(folium.Element(title_html3))
m3.save('outputs/map_2026_v2.html')
print("Saved map_2026_v2.html")
