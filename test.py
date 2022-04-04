import requests
S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
SEARCHPAGE = 'Reina Carvajal'
PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()
resume = DATA['query']['search']
affichage_resume = ""
for i in range(len(resume)):
    affichage_resume += DATA['query']['search'][i]['snippet'].replace("&quot;", "").replace("</span>", "").replace("<span class=\"searchmatch\">", "")

#print(resume)