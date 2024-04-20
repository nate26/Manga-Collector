'''
This script is used to scrape manga volumes and series information from the Crunchyroll
store website.  It retrieves data from JSON files, scrapes the website for new
information, and updates the JSON files with the results.

Functions:
- open_file(file_path): Gets the data from a JSON file and copies it into a return object.
- save_file(file_path, data): Writes the given data to the given file path, and converts
the data into a JSON format.
- scrape_page(url, volumes, series, shop): Scrapes the given URL for manga volumes and series,
and updates the given data structures with the results.
'''

import json
import math
import re
import time
from bs4 import BeautifulSoup
import requests

def open_file(file_path):
    '''Gets the data from a JSON file and copies it into a return object'''
    try:
        with open(file_path, 'r', encoding='UTF-8') as outfile:
            outfile.flush()
            data = json.load(outfile)
            outfile.close()
            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        print('Could not load file ' + file_path + ' ... ending process')
        raise

def save_file(file_path, data):
    '''Writes the given data to the given file path, and converts the data into a JSON format'''
    try:
        with open(file_path, 'w', encoding='UTF-8') as outfile:
            outfile.flush()
            json.dump(data, outfile, indent=4, separators=(',', ': '))
            outfile.close()
    except (FileNotFoundError, TypeError):
        print('Could not save file ' + file_path + ' ... ending process')
        raise

def parse_volume(display_name: str, category: str):
    '''Parses the volume number from the given display name.'''
    if re.search(r' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)
        ).group(0)
    if re.search(r' [()]?Vol[a-z]?[()]? \d+\.?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?Vol[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)
        ).group(0)
    if re.search(r' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)
        ).group(0)
    if re.search(r' [()]?Box Set[()]? \d+\.?\-?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?Box Set[()]? \d+\.?\-?\d*', display_name).group(0)
        ).group(0)
    if re.search(r' [()]?' + category + r'[a-z]?[()]? \d+\.?\-?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?' + category + r'[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)
        ).group(0)
    return None

def scrape_page(soup, volumes, series, shop):
    '''
    Scrapes the given URL for manga volumes and series,
    and updates the given data structures with the results.

    Parameters:
    - soup (str): The Beautiful soup object for a page of the Crunchyroll store website.
    - volumes (dict): A dictionary containing manga volumes information.
    - series (dict): A dictionary containing manga series information.
    - shop (dict): A dictionary containing manga shop information.

    Returns:
    - volumes (dict): Updated dictionary of manga volumes information.
    - series (dict): Updated dictionary of manga series information.
    - shop (dict): Updated dictionary of manga shop information.
    '''
    for item in soup.find_all('div', {'class': 'product'}):
        cr_attr = {
            **json.loads(item.attrs['data-gtmdata']),
            **json.loads(item.find('div', {'class': 'product-tile'}).attrs['data-segmentdata'])
        }
        retail_price = item \
            .find('div', {'class': 'price'}) \
                .find('span', {'class': 'strike-through'}) \
                    .find('span', {'class': 'value'}) \
                        .attrs['content']
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']
        category_id = cr_attr['categoryID'] if 'categoryID' in cr_attr else None
        volume_number = parse_volume(cr_attr['name'], cr_attr['category'])

        product = {
            'isbn': cr_attr['id'],
            'retain_price': retail_price,
            'store_price': cr_attr['price'],
            'stock_status': cr_attr['Inventory_Status'],
            'preorderStatus': cr_attr['pre_order_status'],
            'coupon': cr_attr['coupon']
        }
        shop[cr_attr['id']] = product

        volume = {
            'isbn': cr_attr['id'],
            'series': cr_attr['brand'],
            'name': cr_attr['name'],
            'category': cr_attr['category'],
            'categoryID': category_id,
            'volume': volume_number,
            'url': cr_attr['url'],
            'cover_image': cover_image
        }
        volumes[cr_attr['id']] = volume

        series_volume = {
            'isbn': volume['isbn'],
            'volume': volume['volume'],
            'category': volume['category']
        }

        if cr_attr['brand'] not in series:
            series[cr_attr['brand']] = {
                'name': cr_attr['brand'],
                'cover_image': cover_image,
                'volumes': [series_volume]
            }
        else:
            series_volumes = sorted(
                [
                    *series[cr_attr['brand']]['volumes'],
                    series_volume
                ],
                key = lambda x: (x['category'], x['volume'])
            )
            if series_volumes[0]['isbn'] == volume['isbn']:
                series[cr_attr['brand']]['cover_image'] = cover_image
            series[cr_attr['brand']]['volumes'] = series_volumes

    return volumes, series, shop

volumes_data = open_file('./volumes.json')
series_data = open_file('./series.json')
shop_data = open_file('./shop.json')

PAGE_URL = 'https://store.crunchyroll.com/collections/manga-books/'
first_soup = BeautifulSoup(
    requests.get(PAGE_URL + '?cgid=manga-books&start=0&sz=100', timeout=5).text,
    'html.parser'
)
total_count = int(first_soup.find('div', {'class': 'pagination-text'}).attrs['data-totalcount'])
total_pages = math.ceil(total_count / 100)
print(total_pages)

volumes_new, series_new, shop_new = scrape_page(first_soup, volumes_data, series_data, shop_data)

START = 100
print(f'?cgid=manga-books&start={START}&sz=100')

for i in range(1, total_pages):
    time.sleep(3)
    print(PAGE_URL + f'?cgid=manga-books&start={START}&sz=100')
    # next_soup = BeautifulSoup(
    #     requests.get(PAGE_URL + f'?cgid=manga-books&start={START}&sz=100', timeout=5).text,
    #     'html.parser'
    # )
    # volumes_new, series_new, shop_new = scrape_page(next_soup, volumes_new, series_new, shop_new)
    START += 100

save_file('./volumes.json', volumes_new)
save_file('./series.json', series_new)
save_file('./shop.json', shop_new)
