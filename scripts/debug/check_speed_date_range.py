import requests
import pandas as pd

URL = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"

# Check the oldest and newest data_as_of values actually available
oldest = requests.get(URL, params={"$order": "data_as_of ASC", "$limit": 5}).json()
newest = requests.get(URL, params={"$order": "data_as_of DESC", "$limit": 5}).json()

print("Oldest records:")
for r in oldest:
    print(" ", r.get("data_as_of"))

print("\nNewest records:")
for r in newest:
    print(" ", r.get("data_as_of"))