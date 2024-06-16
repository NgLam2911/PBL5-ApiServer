import requests

url = "http://nglam.xyz/api/v2/sensor"

response = requests.post(url, params={
    "food_weight": 100,
    "water_weight": 100,
})

print(response.json())
print(response.elapsed.total_seconds() * 1000)  # Convert to milliseconds