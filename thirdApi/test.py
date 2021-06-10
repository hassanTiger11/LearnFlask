import requests
BASE = "http://127.0.0.1:5000/"

data = [{"name": "how to make chocolate chip", "views": 2000, "likes": 2},
    {"name": "Python REST api", "views": 2000, "likes": 2},
    {"name": "stuck in the middle", "views": 2000, "likes": 2},

]


for elem in range(len(data)):
    response = requests.put(BASE+"video/"+str(elem), data[elem]) 
    print(response.json())


for elem in range(len(data)):
    response = requests.get(BASE+"video/"+str(elem))
    print(response.json())

'''
for elem in range(len(data)):
    response = requests.delete(BASE+"video/"+str(elem))
    print(response.__str__)
'''


