import requests
BASE = "http://127.0.0.1:5000/"

data = {'name': 'zack'}
reward= {"name": "zack", "reward": "infinte chocolate chips"} 

response = requests.put(BASE+"/log", data)
print(response.json())

response = requests.post(BASE+"/log", reward)
if response:
    print(response.json()) 


response = requests.get(BASE+"/log")
print(response.json())
