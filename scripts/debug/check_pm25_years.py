import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/c3uy-2p5r.json"

resp = requests.get(URL, params={
    "$where": "name = 'Fine particles (PM 2.5)' AND geo_type_name = 'CD'",
    "$select": "distinct time_period",
})
print(resp.json())