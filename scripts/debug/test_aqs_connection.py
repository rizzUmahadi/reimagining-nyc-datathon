import requests

EMAIL = "riyajalmahadi@gmail.com"
KEY = "tealkit53"

url = "https://aqs.epa.gov/data/api/list/states"
params = {"email": EMAIL, "key": KEY}

resp = requests.get(url, params=params)
print("Status:", resp.status_code)
print(resp.json())