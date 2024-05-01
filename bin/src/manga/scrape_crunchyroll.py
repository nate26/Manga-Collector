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

import datetime
import json
import math
import os
import re
from bs4 import BeautifulSoup
import requests

# TO DO:
# - cache api calls
# - add more error handling
# - smart match series by brand, title, artist, etc.
# - flag series matches for manual review if less than 100% match
# - get more accurate release dates

log_name = './logs/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

series_cache = {}

def open_file(file_path):
    '''Gets the data from a JSON file and copies it into a return object'''
    info('Loading file ' + file_path + '...')
    try:
        with open(file_path, 'r', encoding='UTF-8') as outfile:
            outfile.flush()
            data = json.load(outfile)
            outfile.close()
            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        error('Could not load file ' + file_path + ' ... ending process')
        raise

def save_file(file_path, data):
    '''Writes the given data to the given file path, and converts the data into a JSON format'''
    info('Saving file ' + file_path + '...')
    try:
        with open(file_path, 'w', encoding='UTF-8') as outfile:
            outfile.flush()
            json.dump(data, outfile, indent=4, separators=(',', ': '))
            outfile.close()
    except (FileNotFoundError, TypeError):
        error('Could not save file ' + file_path + ' ... ending process')
        raise

def log(type: str, message: str):
    '''Writes the given message to a log file.'''
    try:
        with open(log_name, 'a', encoding='UTF-8') as logfile:
            logfile.write(type + ' [' + os.path + '] ' + str(message) + '\n')
            logfile.close()
    except (FileNotFoundError, TypeError):
        print('Could not write to log file... ending process')
        raise

def info(message: str):
    '''Writes the given message to the console and log file as an info log.'''
    log('[INFO]', message)

def warn(message: str):
    '''Writes the given message to the console and log file as an warn log.'''
    log('[WARN]', message)

def error(message: str):
    '''Writes the given message to the console and log file as an error log.'''
    log('[ERROR]', message)

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

def get_series_by_id(series_id: int):
    '''Gets the series information from the given series ID.'''
    info(f'Getting series details for {series_id}...')
    try:
        series_resp = requests.get('https://api.mangaupdates.com/v1/series/' + str(series_id),
                                    timeout=5).json()
        return {
            'series_id': series_resp['series_id'],
            'title': series_resp['title'],
            'associated_titles': [title['title'] for title in series_resp['associated']],
            'url': series_resp['url'],
            'type': series_resp['type']
        }
    except requests.exceptions.RequestException as e:
        error(e)
        error(f'Could not get series details for {series_id}... ending process')
        raise

def search_series(series_name: str, series_type: str):
    '''Gets the series ID from the given series name and format.'''
    info(f'Searching for series ID for ["{series_name}", "{series_type}" ]...')
    search_data = {
        'search': series_name,
        'stype': 'title'
    }
    try:
        series_resp = requests.post('https://api.mangaupdates.com/v1/series/search',
                                    search_data, timeout=5).json()
        for series in [series_resp['results'][0]]: # fix later for match logic
            series_details = get_series_by_id(series['record']['series_id'])
            info('Checking series: ' + json.dumps(series_details))
            if series_details['title'].lower() == series_name.lower() and \
                series_details['type'].lower() == series_type.lower():
                return series_details
            if len([title for title in series_details['associated_titles']
                    if title.lower() == series_name.lower()]) > 0:
                return series_details
    except requests.exceptions.RequestException as e_search:
        error(e_search)
        error(f'Could not get series ID for "{series_name}"... ending process')

    warn(f'Could not find any matching series ID for {series_name}... ending process')
    return {
        'series_id': None,
        'title': None,
        'associated_titles': [],
        'url': None,
        'type': None
    }

def scrape_page(soup, all_volumes, all_series, all_shop):
    '''
    Scrapes the given URL for manga volumes and series,
    and updates the given data structures with the results.

    Parameters:
    - soup (str): The Beautiful soup object for a page of the Crunchyroll store website.
    - all_volumes (dict): A dictionary containing manga volumes information.
    - all_series (dict): A dictionary containing manga series information.
    - all_shop (dict): A dictionary containing manga shop information.

    Returns:
    - all_volumes (dict): Updated dictionary of manga volumes information.
    - all_series (dict): Updated dictionary of manga series information.
    - all_shop (dict): Updated dictionary of manga shop information.
    '''
    for item in soup.find_all('div', {'class': 'product'}):
        # bs4 object to dict
        cr_attr = {
            **json.loads(item.attrs['data-gtmdata']),
            **json.loads(item.find('div', {'class': 'product-tile'}).attrs['data-segmentdata'])
        }
        info('Scraping item... ' + cr_attr['id'] + ' | ' + cr_attr['name'])

        retail_price = item \
            .find('div', {'class': 'price'}) \
                .find('span', {'class': 'strike-through'}) \
                    .find('span', {'class': 'value'}) \
                        .attrs['content']
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']
        category_id = cr_attr['categoryID'] if 'categoryID' in cr_attr else None

        # # check if the item is valid
        # if not filter_item(cr_attr):
        #     break

        volume_number = parse_volume(cr_attr['name'], cr_attr['category'])

        # get the product
        shop_id = cr_attr['id'] + '-crunchyroll'
        product = {
            'isbn': cr_attr['id'],
            'retain_price': retail_price,
            # split into mega fans (10% off) and ultamate fans (15% off)
            'store_price': cr_attr['price'],
            'stock_status': cr_attr['Inventory_Status'],
            'coupon': cr_attr['coupon'],
            'is_on_sale': item.find('div', {'class': 'sale'}) is not None,
        }
        all_shop[shop_id] = product

        category_conversion = {
            '': None,
            'light-novels': 'novel',
            'manhwa': 'manhwa',
            'manhua': 'manhua',
            'novels': 'novel',
            'manga': 'manga'
        }
        series_details = search_series(cr_attr['brand'], category_conversion[cr_attr['category']])

        # get the volume
        volume = {
            'isbn': cr_attr['id'],
            'series': cr_attr['brand'],
            'series_id': series_details['series_id'],
            'name': cr_attr['name'],
            'category': cr_attr['category'],
            'category_id': category_id,
            'volume': volume_number,
            'url': cr_attr['url']
        }
        if cr_attr['id'] in all_volumes:
            # fetch url
            soup_volume = BeautifulSoup(requests.get(volume['url'], timeout=5).text, 'html.parser')
            descriptions = soup_volume.find('div', {'class': 'product-description'}) \
                .find('div', {'class': 'short-description'}) \
                    .find_all('p')
            volume['description'] = '\n'.join([desc.text for desc in descriptions])
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
            all_volumes[cr_attr['id']] = volume
        else:
            all_volumes[cr_attr['id']] = volume

        # update the series
        series_volume = {
            'isbn': volume['isbn'],
            'volume': volume['volume'],
            'category': volume['category']
        }
        if series_details['series_id'] is not None:
            if series_details['series_id'] not in all_series:
                all_series[series_details['series_id']] = {
                    **series_details,
                    'volumes': [series_volume]
                }
            else:
                existing_volumes = [
                    vol['isbn'] for vol in all_series[series_details['series_id']]['volumes']
                ]
                if series_volume['isbn'] not in existing_volumes:
                    series_volumes = sorted(
                        [
                            *all_series[series_details['series_id']]['volumes'],
                            series_volume
                        ],
                        key = lambda x: (x['category'], x['volume'])
                    )
                    all_series[series_details['series_id']]['volumes'] = series_volumes
                else:
                    idx = existing_volumes.index(series_volume['isbn'])
                    all_series[series_details['series_id']]['volumes'][idx] = series_volumes

    return all_volumes, all_series, all_shop

RUN_SCRAPER = True
if RUN_SCRAPER:
    volumes_data = open_file('./volumes.json')
    series_data = open_file('./series.json')
    shop_data = open_file('./shop.json')

    PAGE_BASE_URL = 'https://store.crunchyroll.com/collections/manga-books/?cgid=manga-books'
    CATEGORY_QUERY = '&prefn1=subcategory&prefv1=Novels|Manhwa|Manhua|Light%20Novels|Manga'
    PAGE_URL = PAGE_BASE_URL + CATEGORY_QUERY

    first_soup = BeautifulSoup(
        requests.get(PAGE_URL + '&start=100&sz=100', timeout=5).text,
        'html.parser'
    )
    total_count = int(first_soup.find('div', {'class': 'pagination-text'}).attrs['data-totalcount'])
    total_pages = math.ceil(total_count / 100)
    info('pages to scrape: ' + str(total_pages))

    volumes_new, series_new, shop_new \
        = scrape_page(first_soup, volumes_data, series_data, shop_data)

    START = 100

    # for i in range(1, total_pages):
    #     info('Calling: ' + PAGE_URL + f'&start={START}&sz=100')
    #     # next_soup = BeautifulSoup(
    #     #     requests.get(PAGE_URL + f'&start={START}&sz=100', timeout=5).text,
    #     #     'html.parser'
    #     # )
    #     # volumes_new, series_new, shop_new \
    #     #     = scrape_page(next_soup, volumes_new, series_new, shop_new)
    #     START += 100

    save_file('./volumes.json', volumes_new)
    save_file('./series.json', series_new)
    save_file('./shop.json', shop_new)


# print(search_series('The Summer Hikaru Died', 'manga'))
