from flask import Flask, render_template
import requests
import json
import random
app = Flask(__name__)

#148 pages
@app.route('/', methods=['GET'])
def index():
    req = requests.get('https://api.disneyapi.dev/characters?page=22')#?page=100
    data = json.loads(req.content)
    return render_template('home.html', data=data['data'])

#Zone de tests pour afficher un élément spécifique
@app.route('/spe/<id>', methods=['GET'])
def spe(id):
    req = requests.get('https://api.disneyapi.dev/characters/')#?page=100
    data = json.loads(req.content)
    random_number = random.randint(1, 10)
    return render_template('spe.html', data=data['data'], id=int(id), random_number=random_number)

if __name__ == '__main__':
    app.run(debug=True)