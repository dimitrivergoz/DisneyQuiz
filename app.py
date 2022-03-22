from venv import create
from flask import Flask, render_template
import requests
import json
import random
app = Flask(__name__)

response = requests.get('https://api.disneyapi.dev/characters/')
data = json.loads(response.content)



list_id = []
for i in data['data']:
    list_id.append(i['_id'])

list_name = []
for i in data['data']:
    list_name.append(i['name'])


def create_link(id):
    lien = "https://api.disneyapi.dev/characters"+str(id)
    return lien

#148 pages
@app.route('/', methods=['GET'])
def index():
    lien = "https://api.disneyapi.dev/characters"
    req = requests.get(lien)#?page=100
    data = json.loads(req.content)
    return render_template('home.html', data=data['data'], req=lien)

#Zone de tests pour afficher un élément spécifique
@app.route('/spe/', methods=['GET'])
def spe():
    random_number = random.choice(list_id)
    random_ajout = random.randint(0,5)

    id = random_number
    response = requests.get('https://api.disneyapi.dev/characters/'+str(id))
    data = json.loads(response.content)
    return render_template('spe.html', name=data['name'], url=data['imageUrl'],data=data,list_name=list_name, list_id=list_id,random_ajout=random_ajout, random_number=random_number)



@app.route('/page/', methods=['GET'])
def page():
    random_page = random.randint(0,149)
    response = requests.get('https://api.disneyapi.dev/characters?page='+str(random_page))
    data = json.loads(response.content)
    list_id = []
    for i in data['data']:
        list_id.append(i['name'])
    return render_template('page.html', list_id=data )


if __name__ == '__main__':
    app.run(debug=True)