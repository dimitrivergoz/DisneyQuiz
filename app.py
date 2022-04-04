from venv import create
from flask import Flask, render_template
import requests
import json
import random
import numpy
app = Flask(__name__)

#Liste sur laquelle, nous avons trouvé des problèmes (pas d'image, pas de noms, etc...)
perso_bug_list = [2919, 5156,6747,2516,4885,5305,4324,5889,4081,7282,5591]
def generate_caractere():
    current_pers = {}
    #Nous savons qu'il y a 149 pages en tout sur cette API
    random_page = random.randint(0,148)
    response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
    if response.status_code != 204:
        data = json.loads(response.content)
    else:
        index()
    number = random.randint(0, 40)
    for i in data['data'][:number]:
        if i["films"] != []:
            try:
                current_pers["films"] = random.choice(i['films'])
                current_pers["id"] = i['_id']
                if current_pers["id"] in perso_bug_list:
                    index()
                current_pers["name"] = i['name']
                try:
                    current_pers["url"] = i['imageUrl']
                except KeyError:
                    current_pers["name"] = i['#']
            except KeyError:
                pass
    try:
        print("ID: ",current_pers["id"])
    except KeyError:
        index()

    return current_pers
@app.route('/', methods=['GET'])
def index():

    real_one = generate_caractere()
    false_one = generate_caractere()
    false_two = generate_caractere()
    try:
        prompt_names = [real_one["name"], false_one["name"], false_two["name"]]
        prompt_films = [real_one["films"], false_one["films"], false_two["films"]]
        prompt_films = numpy.random.choice(prompt_films, len(prompt_films), False)   
        prompt_names = numpy.random.choice(prompt_names, len(prompt_names), False)
    except KeyError:
        index()

    return render_template('home.html',current_pers=real_one,prompt_names=prompt_names,prompt_films=prompt_films)


if __name__ == '__main__':
    app.run(debug=True)