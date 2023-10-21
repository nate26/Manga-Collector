import pandas as pd
import requests
import re
import json
import math
import time
from collections.abc import MutableMapping
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
import uuid

mal_types = {
    'Manga': '1',
    'Light Novel': '2',
    'One-Shot': '3',
    'Doujinshi': '4',
    'Manhwa': '5',
    'Manhua': '6',
    'Novel': '8'
}


# items = requests.get('http://localhost:8050/get-library/').json()

# with open('./items.json', 'w') as outfile:
#     outfile.flush()
#     outfile.write(json.dumps(items))
#     outfile.close()



f = open('./items.json', 'r')
f.flush()
all_items = json.load(f).get('items')
f.close()

fs = open('./series.json', 'r')
fs.flush()
series = json.load(fs)
fs.close()

keys = list(all_items.keys())

print(len(series))

def addVolumeToSeriesDB(isbn):
    title = all_items[isbn].get('name')
    if (title[-7:] == 'Omnibus'):
        title = title.replace(' Omnibus', '')
    series_titles = [s['title'] for s in list(series.values())]
    if title not in series_titles:
        id = str(uuid.uuid4())
        series[id] = {
            'title': title,
            'volumes': [isbn]
        }
    else:
        idx = series_titles.index(title)
        series_keys = series.keys()
        series_volumes = series[list(series_keys)[idx]]['volumes']
        series_volumes.append(isbn)
        series_volumes.sort(key=lambda x: datetime.strptime(all_items[x]['release_date'], "%m/%d/%Y") if all_items[x]['release_date'] != '' else '', reverse=False)
        #sort by date

for isbn in keys:
    addVolumeToSeriesDB(isbn)

print(len(series))
with open("series.json", "w") as outfile:
    json.dump(series, outfile)

def getMalSeriesPage(title):
    try:
        format = mal_types[series.get(title)[0].get('details').get('format')]
        url = 'https://myanimelist.net/manga.php?cat=manga&q=' + title.replace(' ','%20') + '&type=' + format
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find_all('div', {'class': 'js-categories-seasonal'})[0]
        trs = table.find_all('tr')[1:]
        tr_url = trs[0].find_all('a', {'class': 'hoverinfo_trigger'})[0].get('href')
        print(tr_url)
        return tr_url
    except:
        print('could not get series on MAL for ' + title)

