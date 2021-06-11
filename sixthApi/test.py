import requests
BASE= "http://127.0.0.1:5000"
responnse = requests.put(BASE+"/pushAuthor", {"name": "Chuck Paluhniuk"})
print(responnse.text)

responnse = requests.put(BASE+"/pushBook/Chuck Paluhniuk", {"title": "Fight Club"})
print(responnse.text)

response = requests.get(BASE+"/getall")
print(response.text)