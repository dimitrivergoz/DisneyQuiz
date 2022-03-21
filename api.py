import requests
import json
response = requests.get('https://api.disneyapi.dev/characters/')
data = json.loads(response.content)

list_id = []
for i in data['data']:
    list_id.append(i['name'])

print(list_id)