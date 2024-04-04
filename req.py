import requests

url = "http://nglam.xyz/upload"
file = {'file': open('images/8dad2539-c834-48cf-b87e-97e09f0efc7c.png', 'rb')}

response = requests.post(url, files=file)
print(response.json())