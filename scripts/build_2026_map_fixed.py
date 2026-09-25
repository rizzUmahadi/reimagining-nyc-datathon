import pandas as pd
import folium

sites = {
    'IS 74': (40.81551, -73.88553, 'Bronx'),
    'IS 52': (40.816, -73.902, 'Bronx'),
    'PFIZER LAB SITE': (40.8679, -73.87809, 'Bronx'),
    'DIVISION STREET': (40.71436, -73.99518, 'Manhattan'),
    'PS 19': (40.73, -73.984, 'Manhattan'),
    'IS 45': (40.7997, -73.93432, 'Manhattan'),
    'CCNY': (40.81976, -73.94825, 'Manhattan'),
}

bronx_epa = pd.read_csv('data/bronx_pm25_epa_2024_2025_2026.csv')
manhattan_epa = pd.read_csv('data/manhattan_pm25_epa_2024_2025_2026.csv')

NYC_BOUNDS = [[40.68, -74.05], [40.90, -73.80]]
m = folium.Map(tiles="OpenStreetMap")
m.fit_bounds(NYC_BOUNDS)

for site, (lat, lon, borough) in sites.items():
    df = bronx_epa if borough == 'Bronx' else manhattan_epa
    vals = df[(df['local_site_name'] == site) & (df['Year'] == 2026)]['arithmetic_mean']
    if vals.empty:
        continue
    avg = vals.mean()
    color = 'darkred' if avg > 8 else ('orange' if avg > 6.5 else 'green')
    folium.CircleMarker(
        location=(lat, lon), radius=22, color='black', weight=2,
        fill=True, fill_color=color, fill_opacity=0.85
    ).add_to(m)
    folium.Marker(
        location=(lat, lon),
        icon=folium.DivIcon(html=f'''<div style="font-size: 14px; font-weight: bold; color: black;
            background: white; padding: 3px 8px; border-radius: 4px; border: 2px solid black;
            transform: translate(25px, -12px); white-space: nowrap;">{site} ({borough})<br>{avg:.1f} ug/m3</div>''')
    ).add_to(m)

legend_html = '''<div style="position: fixed; bottom: 30px; left: 50px; z-index: 9999;
    background: white; padding: 15px; border-radius: 8px; border: 2px solid black; font-size: 14px;">
    <b>What am I looking at?</b><br>
    Each circle is a real government air pollution monitor.<br>
    The number is the average PM2.5 (fine particle pollution) reading, Jan-Jul 2026.<br><br>
    <span style="color:green;">&#9679;</span> Under 6.5 ug/m3 - Lower pollution<br>
    <span style="color:orange;">&#9679;</span> 6.5-8 ug/m3 - Moderate<br>
    <span style="color:darkred;">&#9679;</span> Over 8 ug/m3 - Higher pollution
    </div>'''
m.get_root().html.add_child(folium.Element(legend_html))

title_html = '''<div style="position: fixed; top: 10px; left: 50px; z-index: 9999;
    background: white; padding: 10px 20px; border-radius: 5px; font-size: 20px; font-weight: bold;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">Air Pollution Monitors: Bronx vs Manhattan, 2026</div>'''
m.get_root().html.add_child(folium.Element(title_html))

m.save('outputs/map_2026_fixed.html')
print("Saved outputs/map_2026_fixed.html")
