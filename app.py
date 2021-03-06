from venv import create
from flask import Flask, render_template
import requests
import json
import random
import numpy
app = Flask(__name__)


#Liste sur laquelle, nous avons trouvé des problèmes (pas d'image, pas de noms, etc...)
perso_bug_list = [2919, 5156,6747,2516,4885,5305,4324,5889,4081,7282,5591,2348,4567,486]
def getdata():
    random_page = random.randint(0,148)
    response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
    data = json.loads(response.content)
    return data

def generate_caractere():
    current_pers = {}
    #Nous savons qu'il y a 149 pages en tout sur cette API
    data = getdata()
    number = random.randint(1, 48)
    for i in data['data'][::number]:
        if i["films"] != [] and i['name'] != "":
            current_pers["id"] = i['_id']
            current_pers["name"] = i['name']
            current_pers["films"] = random.choice(i['films'])
            try:
                current_pers["url"] = i['imageUrl']
            except KeyError:
                perso_bug_list.append(i['_id'])
                generate_caractere()
    return current_pers
  
def api_qwant(real_one_nom, real_one_film):
    query = "scene film disney "+ real_one_film
    r = requests.get("https://api.qwant.com/v3/search/images",
        params={
            'count': 50,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'offset': 0,
            'device': 'desktop'
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )
    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    return urls[0]

@app.route('/', methods=['GET'])
def index():
    prompt_names = []
    real_one = {}
    false_one = {}
    false_two = {}
    while real_one == {}:
        try:
            real_one = generate_caractere()
        except json.decoder.JSONDecodeError:
            try:
                real_one = generate_caractere()
            except json.decoder.JSONDecodeError:
                index()
    while false_one == {}:
        try:
            false_one = generate_caractere()
        except json.decoder.JSONDecodeError:
            try:
                false_one = generate_caractere()
            except json.decoder.JSONDecodeError:
                index()
    while false_two == {}:
        try:
            false_two = generate_caractere()
        except json.decoder.JSONDecodeError:
            try:
                false_two = generate_caractere()
            except json.decoder.JSONDecodeError:
                index()
    if real_one["name"] == false_one["name"] or false_one["name"] == false_two["name"]:
        false_one = "Voyage à l'ESILV"
    elif real_one["name"] ==  false_two["name"]:
        false_two["name"] = "Je repars chez moi à 11h15"
    print("Noms générés\n",real_one,"\n", false_one,"\n", false_two)
    prompt_names = [real_one["name"], false_one["name"], false_two["name"]]
    prompt_films = [real_one["films"], false_one["films"], false_two["films"]]
    prompt_films = numpy.random.choice(prompt_films, len(prompt_films), False)   
    prompt_names_after = numpy.random.choice(prompt_names, len(prompt_names), False)
    retour_image = api_qwant(real_one["name"],real_one["films"])
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
    affichage_resume = affichage_resume[:3]
    response = requests.get('http://www.omdbapi.com/?t='+real_one["films"]+'&plot=full&apikey=457ff858')
    try:
        data_from_movie = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        pass
    prompt_films = numpy.random.choice(prompt_films, len(prompt_films), False)  
    print("Personnage affiché: ID=",real_one['id'])
    len_affichage_resume = len(affichage_resume)
    affichage_resume = affichage_resume[:round(len_affichage_resume/3)] 
    try:
        number_of_type = len(data_from_movie['Genre'].split())
    except KeyError:
        number_of_type = 0
    return render_template('index.html',retour_image=retour_image.replace(" ",""),number_of_type=number_of_type,len_affichage_resume=len_affichage_resume, data_from_movie=data_from_movie, current_pers=real_one,prompt_names=prompt_names_after,prompt_films=prompt_films,loading_page=resume,r=DATA,affichage_resume=affichage_resume)


if __name__ == '__main__':
    app.run(debug=True)
