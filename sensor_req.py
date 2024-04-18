import requests

url = "http://192.168.0.101/loadcell"

result = requests.get(url)
print(result.text)