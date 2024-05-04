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
import logging
import math
import re
from datetime import datetime
from xml.dom import NotFoundErr
import requests
from bs4 import BeautifulSoup

# TO DO:
# - add more error handling
# - smart match series by brand, title, artist, etc.
# - flag series matches for manual review if less than 100% match
# - add more shops
# - fix getting additional images
# - enable saving between volumes
# - fix amazon stock status

series_cache = {}

logging.basicConfig(
    filename='./logs/' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log',
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def open_file(file_path):
    '''Gets the data from a JSON file and copies it into a return object'''
    logger.info('Loading file %s...', file_path)
    try:
        with open(file_path, 'r', encoding='UTF-8') as outfile:
            outfile.flush()
            data = json.load(outfile)
            outfile.close()
            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        logger.critical('Could not load file %s ... ending process', file_path)
        raise

def save_file(file_path, data):
    '''Writes the given data to the given file path, and converts the data into a JSON format'''
    logger.info('Saving file %s...', file_path)
    try:
        with open(file_path, 'w', encoding='UTF-8') as outfile:
            outfile.flush()
            json.dump(data, outfile, indent=4, separators=(',', ': '))
            outfile.close()
    except (FileNotFoundError, TypeError):
        logger.critical('Could not save file %s ... ending process', file_path)
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

def get_series_data(isbn: str, series_name: str, category: str, all_series, all_volumes):
    '''Gets the series information from the given series name and format.'''
    if isbn in all_volumes and all_volumes[isbn]['series_id'] in all_series:
        logger.info('Series found in data... using that instead: %s %s',
                    series_name, all_volumes[isbn]['series_id'])
        return all_series[all_volumes[isbn]['series_id']]
    logger.info('Series not found in data... searching for series ID: %s', series_name)
    category_conversion = {
        '': None,
        'light-novels': 'novel',
        'manhwa': 'manhwa',
        'manhua': 'manhua',
        'novels': 'novel',
        'manga': 'manga'
    }
    return search_series(series_name, category_conversion[category])

def get_series_by_id(series_id: str):
    '''Gets the series information from the given series ID.'''
    logger.info('Getting series details for %s...', series_id)
    try:
        if series_id in series_cache:
            series_resp = series_cache[series_id]
            logger.info('Pulled series from local cache: %s', json.dumps(series_resp))
        else:
            series_resp = requests.get('https://api.mangaupdates.com/v1/series/' + series_id,
                                    timeout=5).json()
            series_cache[series_id] = series_resp
            logger.info('Added series to local cache: %s', json.dumps(series_resp))
        return {
            'series_id': str(series_resp['series_id']),
            'title': series_resp['title'],
            'associated_titles': [title['title'] for title in series_resp['associated']],
            'url': series_resp['url'],
            'type': series_resp['type']
        }
    except requests.exceptions.RequestException as e:
        logger.error(e)
        logger.error('Could not get series details for %s... ending process', series_id)
        raise

def search_series(series_name: str, series_type: str):
    '''Gets the series ID from the given series name and format.'''
    logger.info('Searching for series ID for ["%s", "%s" ]...', series_name, series_type)
    search_data = {
        'search': series_name,
        'stype': 'title'
    }
    try:
        series_resp = requests.post('https://api.mangaupdates.com/v1/series/search',
                                    search_data, timeout=5).json()
        for series in [series_resp['results'][0]]: # fix later for match logic
            series_details = get_series_by_id(str(series['record']['series_id']))
            logger.info('Checking series: %s', json.dumps(series_details))
            if series_details['title'].lower() == series_name.lower() and \
                series_details['type'].lower() == series_type.lower():
                return series_details
            if len([title for title in series_details['associated_titles']
                    if title.lower() == series_name.lower()]) > 0:
                return series_details
    except requests.exceptions.RequestException as e_search:
        logger.error(e_search)
        logger.error('Could not get series ID for "%s"... ending process', series_name)

    logger.warning('Could not find any matching series ID for "%s"... ending process', series_name)
    return {
        'series_id': None,
        'title': None,
        'associated_titles': [],
        'url': None,
        'type': None
    }

def get_isbn_details(soup_isbn_data):
    '''Gets the details from the given ISBN soup object.'''
    details = {
        'release_date': None,
        'publisher': None,
        'format': None,
        'pages': None,
        'authors': None
    }
    try:
        text_tags = soup_isbn_data.find('div', {'class': 'book-info'}).find_all('dt')
        for tag in text_tags:
            if 'Released:' in tag.text and details['release_date'] is None:
                release_date = tag.text.split(': ')[1]
                try:
                    parsed_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', release_date.strip())
                    details['release_date'] = \
                        str(datetime.strptime(parsed_date, '%B %d, %Y').date())
                    logger.info('Found release date: %s', details['release_date'])
                except ValueError:
                    logger.error('Release date is not in correct format... %s', release_date)
            if 'Publisher:' in tag.text and details['publisher'] is None:
                details['publisher'] = tag.text.split(': ')[1].strip()
                logger.info('Found publisher: %s', details['publisher'])
            if 'Format:' in tag.text and details['format'] is None:
                format_details = tag.text.split(': ')[1]
                if '  (' in format_details:
                    split_format = format_details.split('  (')
                    details['format'] = split_format[0].strip()
                    details['pages'] = int(split_format[1].split(' pages')[0].strip())
                    logger.info('Found pages: %s', details['pages'])
                else:
                    details['format'] = format_details.strip()
                logger.info('Found format: %s', details['format'])
            if 'Authors:' in tag.text and details['authors'] is None:
                details['authors'] = tag.text.split(': ')[1].strip()
                logger.info('Found authors: %s', details['authors'])
            if None not in details.values():
                break
        if None in details.values():
            raise NotFoundErr
    except (AttributeError, NotFoundErr) as err:
        logger.warning('Could not find book details from isbn... ending process %s', err)
    return details

def get_shop_data(soup_isbn_data):
    '''Gets all the valid shop details from the given isbn soup object.'''
    shops = []
    try:
        stores = soup_isbn_data.find('div', {'class': 'standard-offers'}).find_all('tr')
        for store in stores:
            try:
                if store.find('td', {'class': 'logo'}).find('span').attrs['title'].strip() \
                    != 'Amazon Mkt Used':
                    raise AttributeError
                logger.info('Found record for shop: Amazon')
                shops.append({
                    'store': 'Amazon',
                    'condition': store.find('td', {'class': 'condition'}).attrs['data-condition'],
                    'url': store.find('td', {'class': 'link'}).text.strip(),
                    'store_price': float(store.find('td', {'class': 'total'})
                        .text.strip().replace('$', '')),
                    'stock_status': None,
                    'coupon': '',
                    'is_on_sale': False
                })
                logger.info('Shop details added: %s', shops[-1])
            except AttributeError:
                continue
    except AttributeError:
        logger.warning('Could not find shop details from isbn... ending process')
    return shops

def isbn_search(isbn: str):
    '''Searches for the given ISBN on the ISBN search website and returns the results.'''
    soup_isbn_data = BeautifulSoup(
        requests.get('https://www.campusbooks.com/search/' + isbn + '?buysellrent=buy', timeout=5)
            .text,
        'html.parser'
    )
    return {
        'details': get_isbn_details(soup_isbn_data),
        'shops': get_shop_data(soup_isbn_data)
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
        isbn = cr_attr['id']
        logger.info('---------- Scraping item... %s | %s ----------', isbn, cr_attr['name'])

        isbn_results = isbn_search(isbn)
        retail_price = item \
            .find('div', {'class': 'price'}) \
                .find('span', {'class': 'strike-through'}) \
                    .find('span', {'class': 'value'}) \
                        .attrs['content']
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']
        category_id = cr_attr['categoryID'] if 'categoryID' in cr_attr else None

        volume_number = parse_volume(cr_attr['name'], cr_attr['category'])

        # get the product
        product = {
            'isbn': isbn,
            'retail_price': float(retail_price),
            'shops': [
                {
                    # split into mega fans (10% off) and ultamate fans (15% off)
                    'store': 'Crunchyroll',
                    'condition': 'New',
                    'url': cr_attr['url'],
                    'store_price': float(cr_attr['price']),
                    'stock_status': cr_attr['Inventory_Status'],
                    'coupon': cr_attr['coupon'],
                    'is_on_sale': item.find('div', {'class': 'sale'}) is not None
                },
                *isbn_results['shops']
            ]
        }
        all_shop[isbn] = product
        logger.info('All shop details added: %s', json.dumps(product))

        series_details = get_series_data(isbn, cr_attr['brand'], cr_attr['category'],
                                         all_series, all_volumes)
        logger.info('Series details: %s', json.dumps(series_details))

        # get the volume
        volume = {
            'isbn': isbn,
            'series': cr_attr['brand'],
            'series_id': series_details['series_id'],
            'name': cr_attr['name'],
            'category': cr_attr['category'],
            'category_id': category_id,
            'volume': volume_number,
            'url': cr_attr['url'],
            **isbn_results['details']
        }
        if isbn in all_volumes:
            # fetch data for description and more images
            soup_volume = BeautifulSoup(requests.get(volume['url'], timeout=5).text, 'html.parser')
            descriptions = soup_volume.find('div', {'class': 'product-description'}) \
                .find('div', {'class': 'short-description'}) \
                    .find_all('p')
            volume['description'] = '\n'.join([desc.text for desc in descriptions])
            volume['cover_images'] = [{ 'name': 'primary', 'url': cover_image }]
            slick_imgs = filter(
                lambda x: 'slick-cloned' not in x.attrs['class'],
                soup_volume.find('div', {'class': 'product-image-carousel'}) \
                    .find_all('div', {'class': 'slick-slide'})
            )
            all_images = [img.find('img').attrs['src'] for img in slick_imgs]
            logger.info('All images: %s for %s', json.dumps(all_images), cr_attr['name'])
            volume['cover_images'].extend(
                [{ 'name': 'alt', 'url': img } for img in all_images if img is not cover_image]
            )
            all_volumes[isbn] = volume
        else:
            all_volumes[isbn] = volume
        logger.info('Volume details added: %s', json.dumps(volume))

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
                logger.info('Added series to data: %s', series_details['series_id'])
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
                    all_series[series_details['series_id']]['volumes'][idx] = series_volume
                logger.info('Series exists, added volume: %s to %s', isbn,
                            json.dumps(all_series[series_details['series_id']]['volumes']))

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
    logger.info('pages to scrape: %s', str(total_pages))

    volumes_new, series_new, shop_new \
        = scrape_page(first_soup, volumes_data, series_data, shop_data)

    START = 100

    # for i in range(1, total_pages):
    #     logger.info('Calling: ' + PAGE_URL + f'&start={START}&sz=100')
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
