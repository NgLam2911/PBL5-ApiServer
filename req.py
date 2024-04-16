import requests

url = "http://nglam.xyz/upload"
file = {'file': open('images/c7e96409-6ade-4cb4-8d30-7413d30c3edd.png', 'rb')}

response = requests.post(url, files=file)
print(response.json())