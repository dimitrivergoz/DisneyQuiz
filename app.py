from venv import create
from flask import Flask, render_template
import requests
import json
import random
app = Flask(__name__)

response = requests.get('https://api.disneyapi.dev/characters/')
data = json.loads(response.content)


@app.route('/', methods=['GET'])
def index():
    random_page = random.randint(0,148)
    response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
    data = json.loads(response.content)
    list_id = []
    list_name = []
    list_url = []
    for i in data['data']:
        list_id.append(i['_id'])
        list_name.append(i['name'])
        try:
            list_url.append(i['imageUrl'])
        except KeyError:
            list_url.append('#')
    aleatoire_number = random.randint(0,len(list_id))
    for_false_name_aleatoire_number = random.randint(0,len(list_id))
    #On vérifie que les 2 nombres générés ne sont pas indiques, de plus, on verifie qu'ils soient pas "out of range"
    if for_false_name_aleatoire_number == aleatoire_number:
        if for_false_name_aleatoire_number > len(list_id):
            for_false_name_aleatoire_number/=2
        else:
            for_false_name_aleatoire_number-1
    id_choisi = list_id[aleatoire_number]
    name_choisi = list_name[aleatoire_number]
    quiz_2nd_name = list_name[for_false_name_aleatoire_number]
    quiz_3nd_name = list_name[-for_false_name_aleatoire_number]
    url_choisi = list_url[aleatoire_number]
    return render_template('page.html', id_choisi=id_choisi,list_url=url_choisi,quiz_2nd_name=quiz_2nd_name,quiz_3nd_name=quiz_3nd_name,  name_choisi=name_choisi,aleatoire_number=aleatoire_number,random_page=random_page)


if __name__ == '__main__':
    app.run(debug=True)