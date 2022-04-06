import requests
import json
import random
import numpy

#Test d'une API dès que le joueur met son choix, un meme apparait en fonction de sa réponse (bonne = Bravo !), (mauvais = BOOOOOh!!)
response = requests.get('https://api.imgflip.com/get_memes')
data = json.loads(response.content)
resume = data['data']['memes']
for i in resume:
    print(i['name'])
    print(i['url'])
