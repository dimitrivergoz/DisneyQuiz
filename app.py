from venv import create
from flask import Flask, render_template
import requests
import json
import random
import numpy
app = Flask(__name__)

response = requests.get('https://api.disneyapi.dev/characters/')
data = json.loads(response.content)

# probleme d'affichage (image) sur #id 2919, 5156, 6747
@app.route('/', methods=['GET'])
def index():
    #On a 148 pages -> on genere un nombre aléatoire pour choisir la page sur lequel le personne sera choisi
    random_page = random.randint(0,148)
    #On cherche la page avec le nb aléatoire généré
    response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
    print('PAGE ========>',random_page)
    data = json.loads(response.content)
    list_id = []
    list_name = []
    list_url = []
    list_film = []
    list_pb = []
    current_list_film = []
    #On met TOUS les éléments présents sur la page dans des listes
    for i in data['data']:
        list_id.append(i['_id'])
        list_name.append(i['name'])
        try:
            list_url.append(i['imageUrl'])
        except KeyError:
            list_url.append('#')
        try:
            list_film.append(i['films'])
        except KeyError:
            list_film.append('#')
            list_pb.append(i)
    #On génére encore une fois un nombre aléatoire pour choisir UN personnage qui sera affiché
    aleatoire_number = random.randint(0,len(list_id)-1)
    #INDEX pour les "faux" noms 
    for_false_name_aleatoire_number = random.randint(0,len(list_id))
    #On vérifie que les 2 nombres générés ne sont pas indiques, de plus, on verifie qu'ils soient pas "out of range"
    if for_false_name_aleatoire_number == aleatoire_number:
        if for_false_name_aleatoire_number > len(list_id):
            for_false_name_aleatoire_number/=2
        else:
            for_false_name_aleatoire_number-1
    id_choisi = list_id[aleatoire_number]
    print('PAGE ========>',id_choisi)

    #On met les infos voulues dans des variables pour les afficher
    name_choisi = list_name[aleatoire_number]
    quiz_2nd_name = list_name[for_false_name_aleatoire_number-1]
    quiz_3rd_name = list_name[-for_false_name_aleatoire_number]
    url_choisi = list_url[aleatoire_number]
    nb_film = 0
    #Compteur pour connaître le nb de films
    for i in list_film:
        if i != []:
            nb_film+=1
            if i not in current_list_film:
                current_list_film.append(i)

    affichage = [name_choisi,quiz_2nd_name, quiz_3rd_name]
    prompt = numpy.random.choice(affichage, len(affichage), False)
    return render_template('index.html',prompt=prompt,current_list_film=current_list_film,nb_film=nb_film,id_choisi=id_choisi,list_film=list_film, list_url=url_choisi,quiz_2nd_name=quiz_2nd_name,quiz_3rd_name=quiz_3rd_name,  name_choisi=name_choisi,aleatoire_number=aleatoire_number,random_page=random_page)


if __name__ == '__main__':
    app.run(debug=True)