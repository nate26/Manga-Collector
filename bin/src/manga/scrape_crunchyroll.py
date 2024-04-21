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

def filter_item(item):
    '''Filters out items that are not manga volumes or series.'''
    if item['categoryID'] in ['art-books', 'manga-bundles', 'graphic-novels',
                                      'light-novels', 'manga', 'manhua', 'manhwa']:
        return True
    else:
        print(f'Item {item["id"]} - {item["name"]} is not in a valid format ' +
            f'({item["categoryID"]}). Skipping...')
        return False

def exists(data, item_id):
    '''Checks if the given item already exists in the given dictionary.'''
    return item_id in data

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

        # bs4 object to dict
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

        # check if the item is valid
        if not filter_item(cr_attr):
            break

        volume_number = parse_volume(cr_attr['name'], cr_attr['category'])

        # get the product
        shop_id = cr_attr['id'] + '-crunchyroll'
        product = {
            'isbn': cr_attr['id'],
            'retain_price': retail_price,
            'store_price': cr_attr['price'], # split into mega fans (10% off) and ultamate fans (15% off)
            'stock_status': cr_attr['Inventory_Status'],
            'coupon': cr_attr['coupon'],
            'is_on_sale': item.find('div', {'class': 'sale'}) is not None,
        }
        shop[shop_id] = product

        # get the volume
        volume = {
            'isbn': cr_attr['id'],
            'series': cr_attr['brand'],
            'name': cr_attr['name'],
            'category': cr_attr['category'],
            'categoryID': category_id,
            'volume': volume_number,
            'url': cr_attr['url']
        }
        if not exists(volumes, cr_attr['id']):
            # fetch url
            soup_volume = BeautifulSoup(requests.get(volume['url'], timeout=5).text, 'html.parser')
            descriptions = soup_volume.find('div', {'class': 'product-description'}) \
                .find('div', {'class': 'short-description'}) \
                    .find_all('p')
            volume['description'] = descriptions[1].text + ' ' + descriptions[0].text
            volume['cover-images'] = [{ 'name': 'primary', 'url': cover_image }]
            slick_imgs = filter(
                lambda x: 'slick-cloned' not in x.attrs['class'],
                soup_volume.find('div', {'class': 'product-image-carousel'}) \
                    .find_all('div', {'class': 'slick-slide'})
            )
            all_images = [img.find('img').attrs['src'] for img in slick_imgs]
            volume['cover-images'].extend(
                [{ 'name': 'alt', 'url': img } for img in all_images if img is not cover_image]
            )
            # get release date more accurately...
            volumes[cr_attr['id']] = volume
        else:
            volumes[cr_attr['id']] = volume

        # get the series
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
