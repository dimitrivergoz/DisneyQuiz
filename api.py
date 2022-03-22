import requests
import json
import random
random_page = random.randint(0,149)
response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
data = json.loads(response.content)
list_id = []
for i in data['data']:
    list_id.append(i['name'])

print(list_id)