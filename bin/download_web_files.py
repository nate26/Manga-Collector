import os
import re
import requests
import unicodedata
from enums.host_enum import HostEnum
from src.data import Data
from time import sleep

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

host = HostEnum.LOCAL
data = Data(host)

items = data.get_library_data()
values = list(items.get('items').values())
counter = 1

for idx, item in enumerate(values):
    print(str(idx) + ' / ' + str(len(values)))
    if counter % 20 == 0:
        sleep(2)
    series = item.get('series') if item.get('series') is not None else 'no_series'
    isbn = item.get('isbn') if item.get('isbn') is not None else 'no_isbn'
    path = './cover_images/' + slugify(series) + '/' + slugify(isbn) + '/'
    
    if len(os.getcwd() + path) > 220:
        print(os.getcwd() + path)
        print(len(os.getcwd() + path))

    if item.get('cover_images') is None:
        print(item.get('isbn'))

    if not os.path.exists(path) and item.get('cover_images') is not None:
        counter += 1
        os.makedirs(path)
        for image in item.get('cover_images'):       
            response = requests.get(image.get('url'))
            with open(path + image.get('name') + '.jpg', 'wb') as f:
                f.write(response.content)
