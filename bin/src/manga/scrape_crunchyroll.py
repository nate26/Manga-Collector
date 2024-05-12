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

import difflib
import json
import logging
import math
import re
from datetime import datetime
from xml.dom import NotFoundErr
import requests
from bs4 import BeautifulSoup

# fix:
# - release_date nulls
# - series title english
# - more info from series data
# - volume names (should not be series names)

# TO DO:
# - add more error handling
# - add more shops
# - get better additional images / better way to get images/descriptions
# - fix amazon stock status
# - find a way to get age ratings / adult tag -> Amazon has this
# - fix b&n query and check if b&n ever has a sale?

RUN_SCRAPER = True
SCRAPE_ALL_PAGES = True

START = 3300

QUERY_ISBN_DB = True
QUERY_CR_FOR_DETAILS = True
QUERY_BARNS_AND_NOBLE = False

# only used if requires a full refresh of all data
FORCE_CR_FOR_DETAILS = True
REFRESH_VOLUME_DETAILS = True
REFRESH_SERIES_DATA = True

# might need to do some memory management here cause it gets big with a lot of data
series_cache = {}

logging.basicConfig(
    filename='./logs/' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log',
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def open_file(file_path):
    '''
    Gets the data from a JSON file and copies it into a return object

    Parameters:
    - file_path (str): The file path to get the data from.

    Returns:
    - dict: The data from the given file path.

    Raises:
    - FileNotFoundError: The file path could not be found.
    - json.JSONDecodeError: The JSON data could not be decoded.
    - TypeError: The data type could not be determined.
    '''
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
    '''
    Writes the given data to the given file path, and converts the data into a JSON format

    Parameters:
    - file_path (str): The file path to save the data to.
    - data: The data to save to the file path.

    Raises:
    - FileNotFoundError: The file path could not be found.
    - TypeError: The data type could not be determined.
    '''
    logger.info('Saving file %s...', file_path)
    try:
        with open(file_path, 'w', encoding='UTF-8') as outfile:
            outfile.flush()
            json.dump(data, outfile, indent=4, separators=(',', ': '))
            outfile.close()
    except (FileNotFoundError, TypeError):
        logger.critical('Could not save file %s ... ending process', file_path)
        raise

def save_all_files(volumes_provided, series_provided, shop_provided):
    '''
    Saves all the given data structures to their respective files.

    Parameters:
    - volumes_provided: The volumes data structure to save to the file.
    - series_provided: The series data structure to save to the file.
    - shop_provided: The shop data structure to save to the file.

    Raises:
    - FileNotFoundError: If a file path could not be found.
    - TypeError: If the data type could not be determined.
    '''
    logger.info('Saving all files...')
    save_file('./volumes.json', volumes_provided)
    save_file('./series.json', series_provided)
    save_file('./shop.json', shop_provided)

def parse_volume(display_name: str, category: str):
    '''
    Parses the volume number from the given display name.

    Parameters:
    - display_name (str): The display name to search for.
    - category (str): The category of the volume to search for.

    Returns:
    - str: The volume number from the given display name. Or None if no volume number is found.
    '''
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
    if re.search(r' [()]?Vol.[a-z]?[()]? \d+\.?\d*', display_name):
        return re.search(
            r'\d+\.?\-?\d*',
            re.search(r' [()]?Vol.[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)
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

def get_series_by_id(series_id: str):
    '''
    Gets the series information from the given series ID.
    
    Parameters:
    - series_id (str): The ID of the series to search for.

    Returns:
    - dict: The series information from the given series ID.

    Raises:
    - requests.exceptions.RequestException: An error occurred while getting the series details.
    '''
    logger.info('Getting series details for %s...', series_id)
    try:
        if series_id in series_cache:
            parsed_series_data = series_cache[series_id]
            logger.info('Pulled series from local cache: %s', json.dumps(parsed_series_data))
        else:
            series_resp = requests.get('https://api.mangaupdates.com/v1/series/' + series_id,
                                    timeout=30).json()
            top_themes = sorted(
                [
                    {
                        'theme': category['category'],
                        'votes': category['votes_plus'] - category['votes_minus']
                    }
                    for category in series_resp['categories']
                    if (category['votes_plus'] - category['votes_minus']) > 0
                ],
                key = lambda x: x['votes'],
                reverse=True
            )[:15]
            parsed_series_data = {
                'series_id': str(series_resp['series_id']),
                'title': series_resp['title'],
                'associated_titles': [title['title'] for title in series_resp['associated']],
                'url': series_resp['url'],
                'category': series_resp['type'],
                'description': series_resp['description'],
                'cover_image': series_resp['image']['url']['original'],
                'genres': [genre['genre'] for genre in series_resp['genres']],
                'themes': top_themes,
                'latest_chapter': series_resp['latest_chapter'],
                'release_status': series_resp['status'],
                'status': 'Complete'  if 'Complete' in series_resp['status'] else \
                    ('Ongoing' if 'Ongoing' in series_resp['status'] else \
                        ('Hiatus' if 'Hiatus' in series_resp['status'] else 'Unknown')),
                'authors': [
                    { 'name': author['name'], 'type': author['type'] }
                    for author in series_resp['authors']
                ],
                'publishers': [
                    { 'name': publisher['publisher_name'], 'type': publisher['type'] }
                    for publisher in series_resp['publishers']
                ],
                'bayesian_rating': series_resp['bayesian_rating'],
                'rank': series_resp['rank']['position']['year'],
                'recommendations': [rec['series_id'] for rec in series_resp['recommendations']]
            }
            series_cache[series_id] = parsed_series_data
            logger.info('Added series to local cache: %s', json.dumps(parsed_series_data))
        return parsed_series_data
    except requests.exceptions.RequestException as e:
        logger.error(e)
        logger.error('Could not get series details for %s... ending process', series_id)
        raise

def set_confidence(current_confidence, new_confidence: float):
    '''
    Sets the confidence level for the given confidence values.
    
    Parameters:
    - current_confidence: The current confidence level.
    - new_confidence (float): The new confidence level.

    Returns:
    - float: The confidence level for the given confidence values.
    '''
    if current_confidence is None:
        return new_confidence
    return max(current_confidence['series_match_confidence'], new_confidence)

def calculate_confidence(series_name: str, title: str):
    '''
    Calculates the confidence level for the given series name and title.

    Parameters:
    - series_name (str): The name of the series to search for.
    - title (str): The title to search for.

    Returns:
    - float: The confidence level for the given series name and title.
    '''
    return 1 - (len([
        li for li in difflib.ndiff(series_name.lower(), title.lower())
        if li[0] != ' '
    ]) / max(len(series_name), len(title)))

def search_series(series_name: str, category: str, volume_name: str):
    '''
    Gets the series ID from the given series name and format.
    
    Parameters:
    - series_name (str): The name of the series to search for.
    - category (str): The category of the series to search for.
    - volume_name (str): The name of the volume to search for.

    Returns:
    - dict: The series information from the given series name and format.
    '''
    category_conversion = {
        '': None,
        'light-novels': 'novel',
        'manhwa': 'manhwa',
        'manhua': 'manhua',
        'novels': 'novel',
        'manga': 'manga'
    }
    series_category = category_conversion[category]
    logger.info('Searching for series ID for ["%s", "%s" ]...', series_name, series_category)
    search_data = {
        'search': series_name,
        'stype': 'title'
    }
    try:
        if series_name is None:
            raise AttributeError('series name is None')

        series_resp = requests.post('https://api.mangaupdates.com/v1/series/search',
                                    search_data, timeout=30).json()
        # only used if no exact match is found
        closest_series_match = None
        for series in [series_resp['results'][0]]:
            series_details = get_series_by_id(str(series['record']['series_id']))
            logger.info('Checking series: %s', json.dumps(series_details))

            # series category must match
            if series_details['category'].lower() == series_category.lower():
                all_titles = [
                    title.lower() for title
                    in [ series_details['title'], *series_details['associated_titles'] ]
                ]

                # check for exact equality in title or associated titles
                if len([
                    title for title
                    in all_titles
                    if title == series_name.lower()
                ]) > 0:
                    series_details['series_match_confidence'] = 1
                    return series_details

                # set first found to match category to a low confidence match
                series_details['series_match_confidence'] = \
                    set_confidence(closest_series_match, 0.1)
                closest_series_match = series_details

                # check for partial equality in title or associated titles
                for title in all_titles:
                    confidence = max(
                        # if series title or associated title is in volume name
                        # case: 'Re:ZERO Ex' in 'Re:Zero Ex Novel Volume 1' = True
                        calculate_confidence(series_name, title),
                        # if series name is in title or associated title, or vice versa
                        # case: 'Re:Zero' in 'Re:ZERO Ex (Novel)' = True
                        calculate_confidence(volume_name, title)
                    )
                    series_details['series_match_confidence'] = \
                        set_confidence(closest_series_match, confidence)
                    closest_series_match = series_details
                    series_details['title'] = title # update title to closest match

        if closest_series_match is not None:
            logger.info('Closest series match with confidence %s: %s',
                        closest_series_match['series_match_confidence'],
                        json.dumps(closest_series_match))
            return closest_series_match
    except (requests.exceptions.RequestException, IndexError, AttributeError) as e_search:
        logger.error(e_search)
        logger.error('Could not get series ID for "%s"... ending process', series_name)

    logger.warning('Could not find any matching series ID for "%s"... ending process', series_name)
    return {
        'series_id': None,
        'title': None,
        'associated_titles': [],
        'url': None,
        'category': None,
        'description': None,
        'cover_image': None,
        'genres': [],
        'themes': [],
        'latest_chapter': None,
        'release_status': None,
        'status': None,
        'authors': [],
        'publishers': [],
        'bayesian_rating': None,
        'rank': None,
        'recommendations': [],
    }

def get_isbn_details(soup_isbn_data):
    '''
    Gets the details from the given ISBN soup object.

    Parameters:
    - soup_isbn_data: The soup object containing the ISBN data.

    Returns:
    - dict: The details from the given ISBN soup object.
    '''
    details = {
        'release_date': None,
        'publisher': None,
        'format': None,
        'pages': None,
        'authors': None,
        'isbn_10': None
    }
    try:
        text_tags = soup_isbn_data.find('div', {'class': 'book-info'}).find_all('dt')
        for tag in text_tags:
            if 'Released:' in tag.text and details['release_date'] is None:
                release_date = tag.text.split(': ')[1]
                try:
                    parsed_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', release_date.strip())
                    date = str(datetime.strptime(parsed_date, '%b %d, %Y').date())
                    if date != datetime.now().strftime('%b %d, %Y'):
                        details['release_date'] = date
                    else:
                        logger.error('Release date is today for future releases (incorrect): %s',
                                     details['release_date'])
                    logger.info('Found release date: %s', details['release_date'])
                except (ValueError, AttributeError) as err:
                    logger.error('Release date is not in correct format... %s', release_date)
                    logger.error(err)
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
            if 'ISBN 10:' in tag.text and details['isbn_10'] is None:
                details['isbn_10'] = tag.text.split(': ')[1].strip()
                logger.info('Found ISBN 10: %s', details['isbn_10'])
            if None not in details.values():
                break
        if None in details.values():
            raise NotFoundErr
    except (AttributeError, NotFoundErr) as err:
        logger.warning('Could not find all book details from isbn... ending process because %s', err)
        logger.warning('Details found: %s', json.dumps(details))
    return details

def get_shop_data(soup_isbn_data, isbn_10: str):
    '''
    Gets all the valid shop details from the given isbn soup object.
    
    Parameters:
    - soup_isbn_data: The soup object containing the ISBN data.
    - isbn_10 (str): The ISBN-10 number to search for.

    Returns:
    - list: The list of shop details for the given ISBN.
    '''
    shops = []
    try:
        stores = soup_isbn_data.find('div', {'class': 'standard-offers'}).find_all('tr')
        for store in stores:
            try:
                if store.find('td', {'class': 'logo'}).find('span').attrs['title'].strip() \
                    != 'Amazon Mkt Used':
                    raise AttributeError('could not find "Amazon Mkt Used" in page')
                logger.info('Found record for shop: Amazon')
                shops.append({
                    'store': 'Amazon',
                    'condition': store.find('td', {'class': 'condition'}).attrs['data-condition'],
                    'url': 'https://www.amazon.com/dp/' + isbn_10,
                    'store_price': float(store.find('td', {'class': 'total'})
                        .text.strip().replace('$', '')),
                    'stock_status': None,
                    'last_stock_update': None,
                    'coupon': '',
                    'is_on_sale': False
                })
                logger.info('Shop details added: %s', shops[-1])
            except AttributeError:
                continue
    except AttributeError as err:
        logger.warning('Could not find shop details from isbn... ending process because %s', err)
    return shops

def isbn_search(isbn: str):
    '''
    Searches for the given ISBN on the ISBN search website and returns the results.

    Parameters:
    - isbn (str): The ISBN to search for.

    Returns:
    - dict: The results of the ISBN search.
    '''
    soup_isbn_data = BeautifulSoup(
        requests.get('https://www.campusbooks.com/search/' + isbn + '?buysellrent=buy', timeout=30)
            .text,
        'html.parser'
    )
    isbn_details = get_isbn_details(soup_isbn_data)
    return {
        'details': isbn_details,
        'shops': get_shop_data(soup_isbn_data, isbn_details['isbn_10'])
    }

def get_barnes_and_noble_data(isbn: str, vol_shop_data: list):
    '''
    Gets the Barnes & Noble data for the given ISBN.

    Parameters:
    - isbn (str): The ISBN to search for.
    - vol_shop_data (list): The list of shop data for the given volume.

    Returns:
    - dict: The Barnes & Noble data for the given ISBN.
    '''
    url = 'https://barnesandnoble.com/w/?ean=' + isbn
    logger.info('Getting Barnes & Noble data for %s...', isbn)
    soup_bn_data = BeautifulSoup(
        requests.get(url, timeout=30).text,
        'html.parser'
    )
    formats = soup_bn_data.find_all('div', {'class': 'pdp-commerce-format'})
    valid_format = [format for format in formats if 'Paperback' in format.text]
    store_price = float(valid_format[0].find('div', {'class': 'format-price'})
                        .text.strip().replace('$', '')) \
                            if len(valid_format) > 0 else None
    stock_status = soup_bn_data.find('div', {'class': 'purchase-add-to-cart'}) \
        .find('div', {'class': 'add-to-cart-button'}).attrs['value']
    existing_bn_data = list(filter(lambda x: x['store'] == 'Barnes & Noble', vol_shop_data))
    is_new_entry = len(existing_bn_data) == 0
    existing_stock_status = existing_bn_data[0]['stock_status'] \
        if not is_new_entry else None
    return {
        'store': 'Barnes & Noble',
        'condition': 'New',
        'url': url,
        'store_price': store_price,
        'stock_status': stock_status,
        'last_stock_update': str(datetime.now()) \
            if is_new_entry and stock_status == existing_stock_status \
                else existing_bn_data[0]['last_stock_update'],
        'coupon': '',
        'is_on_sale': False
    }

def scrape_page(item, all_volumes, all_series, all_shop):
    '''
    Scrapes the given URL for manga volumes and series,
    and updates the given data structures with the results.

    Parameters:
    - item (dict): The Beautiful soup object for an item in the Crunchyroll store website.
    - all_volumes (dict): A dictionary containing manga volumes information.
    - all_series (dict): A dictionary containing manga series information.
    - all_shop (dict): A dictionary containing manga shop information.

    Returns:
    - all_volumes (dict): Updated dictionary of manga volumes information.
    - all_series (dict): Updated dictionary of manga series information.
    - all_shop (dict): Updated dictionary of manga shop information.
    '''
    # bs4 object to dict
    cr_attr = {
        **json.loads(item.attrs['data-gtmdata']),
        **json.loads(item.find('div', {'class': 'product-tile'}).attrs['data-segmentdata'])
    }
    isbn = cr_attr['id']
    logger.info('---------- Scraping item... %s | %s ----------', isbn, cr_attr['name'])

    is_new_volume = isbn not in all_volumes
    if (QUERY_ISBN_DB and not is_new_volume) or is_new_volume:
        isbn_results = isbn_search(isbn)
    else:
        isbn_results = { 'details': {}, 'shops': [] }
        logger.info('Volume exists, ISBN search skipped...')

    retail_price = max([
        price.attrs['content']
        for price in
        item.find('div', {'class': 'price'}) \
            .find_all('span', {'class': 'value'})
    ])
    cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']

    volume_number = parse_volume(cr_attr['name'], cr_attr['category'])

    # get the product
    stock_status = cr_attr['Inventory_Status']
    # update if stock status is different or new volume
    last_stock_update = str(datetime.now()) \
        if is_new_volume or stock_status != all_shop[isbn]['shops'][0]['stock_status'] \
            else all_shop[isbn]['shops'][0]['last_stock_update']
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
                'last_stock_update': last_stock_update,
                'coupon': cr_attr['coupon'],
                'is_on_sale': item.find('div', {'class': 'sale'}) is not None
            },
            *isbn_results['shops']
        ]
    }
    # get barnes and noble data
    if QUERY_BARNS_AND_NOBLE:
        try:
            bn_data = get_barnes_and_noble_data(isbn,
                [] if is_new_volume else all_shop[isbn]['shops'])
            logger.info('Barnes & Noble data: %s', json.dumps(bn_data))
            product['shops'].append(bn_data)
        except (requests.exceptions.RequestException, IndexError) as e:
            logger.error(e)
            logger.error('Could not get Barnes & Noble data for %s... ending process', isbn)
    all_shop[isbn] = product
    logger.info('All shop details added: %s', json.dumps(product))

    # get the series data
    brand_name = cr_attr['brand']
    # query series if volume is new or series is not in data
    if not REFRESH_SERIES_DATA and isbn in all_volumes \
        and all_volumes[isbn]['series_id'] in all_series:
        logger.info('Series found in data... using that instead: %s %s',
                    brand_name, all_volumes[isbn]['series_id'])
        series_details = all_series[all_volumes[isbn]['series_id']]
    elif is_new_volume or REFRESH_SERIES_DATA:
        logger.info('Series not found in data or forcefully updating series...' +
                    ' searching for series ID: %s', brand_name)
        series_details = search_series(brand_name, cr_attr['category'], cr_attr['name'])
    else:
        logger.info('Skipping series search on existing volume: %s', isbn)
        series_details = { 'series_id': None, 'title': cr_attr['brand'] }
    logger.info('Series details: %s', json.dumps(series_details))
    series_id = series_details['series_id']

    # get the volume
    volume = {
        'isbn': isbn,
        'brand': brand_name,
        'series': series_details['title'],
        'series_id': series_id,
        'display_name': cr_attr['name'],
        'name': series_details['title'] or brand_name, #fix?
        'category': cr_attr['category'],
        'volume': volume_number,
        'url': cr_attr['url'],
        'record_added_date': str(datetime.now()) if is_new_volume \
            else all_volumes[isbn]['record_added_date'],
        'record_updated_date': str(datetime.now()),
        **isbn_results['details']
    }

    if is_new_volume \
        or (REFRESH_VOLUME_DETAILS and (QUERY_CR_FOR_DETAILS or FORCE_CR_FOR_DETAILS)):
        volume['cover_images'] = [{ 'name': 'primary', 'url': cover_image }]
        # fetch data for description and more images
        if (QUERY_CR_FOR_DETAILS and not is_new_volume) \
            or FORCE_CR_FOR_DETAILS:
            logger.info('Scraping CR page for description and more cover images: %s', isbn)
            soup_volume = BeautifulSoup(
                requests.get(volume['url'], timeout=30).text,
                'html.parser'
            )
            # get the release date
            preorder_soup = soup_volume.find('div', {'class': 'pre-order-street-date'})
            if preorder_soup is not None:
                preorder_text = soup_volume.find('div', {'class': 'pre-order-street-date'}).text
                if 'Release date:' in preorder_text:
                    parsed_preorder_date = preorder_text.replace('Release date:', '').strip()
                    volume['release_date'] = str(datetime.strptime(
                        parsed_preorder_date, '%m/%d/%Y').date())
                else:
                    parsed_preorder_date = preorder_text.replace('ESTIMATED TO SHIP', '') \
                        .replace('Ship date is an estimate and not guaranteed', '') \
                            .replace('Pre-order FAQ', '') \
                                .strip()
                    volume['release_date'] = str(datetime.strptime(
                        parsed_preorder_date, '%B %d, %Y').date())
            # get the description
            descriptions = soup_volume.find('div', {'class': 'product-description'}) \
                .find('div', {'class': 'short-description'}) \
                    .find_all('p')
            volume['description'] = '\n'.join([desc.text for desc in descriptions])
            # get the thumbnail carousel images
            carousel = soup_volume.find_all('div', {'class': 'slick-paging-image-container'})
            all_images = [
                img.find('img', {'class': 'img-fluid'}).attrs['src'] for img in carousel
            ]
            logger.info('All images: %s for %s', json.dumps(all_images), cr_attr['name'])
            volume['cover_images'].extend(
                [
                    { 'name': 'thumbnail', 'url': img } for img in all_images
                    if img is not cover_image # will not catch because they are thumbnails now
                ]
            )
        else:
            logger.info('Volume details already exist... skipping CR page scraping: %s', isbn)
        all_volumes[isbn] = volume
    # override existing volume details with new volume details
    elif REFRESH_VOLUME_DETAILS:
        volume['series_id'] = all_volumes[isbn]['series_id']
        all_volumes[isbn] = volume
        logger.info('Volume details refreshed: %s', json.dumps(volume))
    else:
        logger.info('Volume exists, not refreshing volume details...')
    logger.info('Volume details added: %s', json.dumps(volume))

    # update the series
    series_volume = {
        'isbn': volume['isbn'],
        'volume': volume['volume'],
        'category': volume['category']
    }
    if series_id is not None:
        if series_id not in all_series:
            all_series[series_id] = {
                **series_details,
                'volumes': [series_volume]
            }
            logger.info('Added series to data: %s', series_id)
        else:
            existing_volumes = [
                vol['isbn'] for vol in all_series[series_id]['volumes']
            ]
            if series_volume['isbn'] not in existing_volumes:
                series_volumes = sorted(
                    [
                        *all_series[series_id]['volumes'],
                        series_volume
                    ],
                    key = lambda x: (
                        x['category'],
                        -1
                        if x['volume'] is None
                        else (
                            int(x['volume'].split('-')[0])
                            if '-' in x['volume']
                            else int(x['volume'])
                        )
                    )
                )
                all_series[series_id]['volumes'] = series_volumes
                logger.info('Series exists, added volume: %s to %s', isbn,
                            json.dumps(all_series[series_id]['volumes']))
            else:
                idx = existing_volumes.index(series_volume['isbn'])
                all_series[series_id]['volumes'][idx] = series_volume
                logger.info('Series exists, updated volume: %s to %s', isbn,
                            json.dumps(all_series[series_id]['volumes']))
            if REFRESH_SERIES_DATA:
                all_series[series_id] = { **all_series[series_id], **series_details }
                logger.info('Series details forcefully updated: %s',
                            json.dumps(all_series[series_id]))

    return all_volumes, all_series, all_shop

if RUN_SCRAPER:
    volumes_data = open_file('./volumes.json')
    series_data = open_file('./series.json')
    shop_data = open_file('./shop.json')

    PAGE_BASE_URL = 'https://store.crunchyroll.com/collections/manga-books/?cgid=manga-books'
    CATEGORY_QUERY = '&prefn1=subcategory&prefv1=Novels|Manhwa|Manhua|Light%20Novels|Manga'
    PAGE_URL = PAGE_BASE_URL + CATEGORY_QUERY

    logger.info('Calling: %s&start=%s&sz=100', PAGE_URL, START)
    first_soup = BeautifulSoup(
        requests.get(PAGE_URL + f'&start={START}&sz=100', timeout=30).text,
        'html.parser'
    )
    total_count = int(first_soup.find('div', {'class': 'pagination-text'}).attrs['data-totalcount'])
    total_pages = math.ceil(total_count / 100)
    completed = 0
    logger.info('pages to scrape: %s', str(total_pages))

    if SCRAPE_ALL_PAGES:

        for i in range(0, total_pages):
            logger.info('Calling: %s&start=%s&sz=100', PAGE_URL, START)

            if START == 0:
                next_soup = first_soup
            else:
                next_soup = BeautifulSoup(
                    requests.get(PAGE_URL + f'&start={START}&sz=100', timeout=30).text,
                    'html.parser'
                )

            for item in next_soup.find_all('div', {'class': 'product'}):
                logger.info('Starting item %s from page %s of %s', i, total_pages)

                volumes_new, series_new, shop_new \
                    = scrape_page(item, volumes_new, series_new, shop_new)

                # save each volume to file
                save_all_files(volumes_new, series_new, shop_new)

                # update progress bar
                completed += 1
                progress = round((completed / total_count) * 50)
                remaining = 50 - progress
                percentage = round((completed / total_count) * 100, ndigits=2)
                print('progress: |' + ''
                        .join(['=' for _ in range(progress)]) + ''
                        .join(['-' for _ in range(remaining)]) +
                        '| ' + str(percentage) + '%',
                        end='\r')

            START += 100

# print(calculate_confidence(
    # 'Re:ZERO',
    # 'Re:ZERO -Starting Life in Another World- Ex (Novel)')),
# print(calculate_confidence(
    # 'Re:ZERO Starting Life in Another World Ex Novel Volume 1',
    # 'Re:ZERO -Starting Life in Another World- Ex (Novel)'))
