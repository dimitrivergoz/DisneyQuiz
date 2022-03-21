import requests
import json

response = requests.get('https://api.disneyapi.dev/characters')

for data in response.json()['data']:
    print(data['name'])
    if not(data['films']):
        print("=======> Aucun film trouvé, Besoin d'appeler WIKIPEDIA API")
    else:
        print("=======> ",data['films'])