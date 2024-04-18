import requests

url = "http://nglam.xyz/api/sensor"
args = {"food_weight": 35}
response = requests.post(url, params=args)
print(response.request.url)
print(response.request.body)
print(response.request.headers)
print(response.json())