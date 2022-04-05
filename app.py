from venv import create
from flask import Flask, render_template
import requests
import json
import random
import numpy
app = Flask(__name__)

random_page = random.randint(0,148)
response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
data = json.loads(response.content)
#Liste sur laquelle, nous avons trouvé des problèmes (pas d'image, pas de noms, etc...)
perso_bug_list = [2919, 5156,6747,2516,4885,5305,4324,5889,4081,7282,5591,2348,4567]
def generate_caractere():
    current_pers = {}
    #Nous savons qu'il y a 149 pages en tout sur cette API
    number = random.randint(0, 40)
    print("=============================================>",data['data'][:number])
    for i in data['data'][::number]:
        if i["films"] != [] and i['name'] != "":
            current_pers["id"] = i['_id']
            current_pers["name"] = i['name']
            current_pers["films"] = random.choice(i['films'])
            try:
                current_pers["url"] = i['imageUrl']
            except KeyError:
                current_pers["url"] = "#"
    return current_pers

@app.route('/', methods=['GET'])
def index():
    prompt_names = []
    real_one = generate_caractere()
    false_one = generate_caractere()
    false_two = generate_caractere()
    while real_one == {}:
        real_one = generate_caractere()
    while false_one == {}:
        false_one = generate_caractere()
    while false_two == {}:
        false_two = generate_caractere()
    prompt_names = [real_one["name"], false_one["name"], false_two["name"]]
    prompt_films = [real_one["films"], false_one["films"], false_two["films"]]
    print("Prompt_films: ",prompt_films)
    print("prompt_names: ",prompt_names)
    prompt_films = numpy.random.choice(prompt_films, len(prompt_films), False)   
    prompt_names_after = numpy.random.choice(prompt_names, len(prompt_names), False)

    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    SEARCHPAGE = real_one["name"] + " " + real_one["films"]
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    resume = DATA['query']['search']
    affichage_resume = []
    for i in range(len(resume)):
        affichage_resume.append(DATA['query']['search'][i]['snippet'].replace("&quot;", "").replace("</span>", "").replace("<span class=\"searchmatch\">", ""))

    affichage_resume = ' '.join(affichage_resume).split('.')
    response = requests.get('http://www.omdbapi.com/?t='+real_one["films"]+'&plot=full&apikey=457ff858')
    try:
        data_from_movie = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        pass
    prompt_films = numpy.random.choice(prompt_films, len(prompt_films), False)  
    print("Personnage affiché: ID=",real_one['id'])
    len_affichage_resume = len(affichage_resume) 
    return render_template('index.html',len_affichage_resume=len_affichage_resume, data_from_movie=data_from_movie, current_pers=real_one,prompt_names=prompt_names_after,prompt_films=prompt_films,loading_page=resume,r=DATA,affichage_resume=affichage_resume)


if __name__ == '__main__':
    app.run(debug=True)

