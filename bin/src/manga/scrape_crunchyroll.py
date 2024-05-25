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
from datetime import datetime
import traceback
import requests
from bs4 import BeautifulSoup
import websockets

from run_websocket import CONNECTIONS
from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.util.local_dao import LocalDAO
from src.manga.scrape_barnes_and_noble import ScrapeBarnesAndNoble
from src.manga.scrape_isbn import ScrapeISBN
from src.manga.series_search import SeriesSearch
from src.data import Data
from src.util.manga_logger import MangaLogger

# fix:
# - some series are not getting caught, ex: "Spice and Wolf"
# - volume names (should not be series names)

# TO DO:
# - re-check release dates for only pre-orders*****
# - add more error handling
# - add more shops
# - get better additional images / better way to get images/descriptions
# - fix amazon stock status
# - find a way to get age ratings / adult tag -> Amazon has this
# - fix b&n query and check if b&n ever has a sale?
# - memory management on series_cache?

class ScrapeCrunchyroll:
    '''
    A class used to scrape manga volumes and series information from the Crunchyroll store website.
    
    ...
    
    Attributes
    ----------
    logger : MangaLogger
        a logging utility for info, warning, and error logs
    scrape_isbn : ScrapeISBN
        a utility to scrape ISBN data
    series_search : SeriesSearch
        a utility to search for series data
    scrape_barnes_and_noble : ScrapeBarnesAndNoble
        a utility to scrape Barnes & Noble data
    data : Data
        a utility to access book data
    
    Methods
    -------
    parse_volume(display_name, category)
        Parses the volume number from the given display name.
    scrape_page(item, all_volumes, all_series, all_shop)
        Scrapes the given URL for manga volumes and series, and updates the given data structures
        with the results.
    run_scraper()
        Scrapes the Crunchyroll store website for manga volumes and series information.
    '''

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)
        self.host = host
        self.scrape_isbn = ScrapeISBN(host)
        self.series_search = SeriesSearch(host)
        self.scrape_barnes_and_noble = ScrapeBarnesAndNoble(host)
        self.data = Data(host)
        self.local_dao = LocalDAO(host)

        self.enable_scrape = True
        self.scrape_all_pages = True

        self.query_isbn_db = False
        self.query_cr_for_details = False
        self.query_barnes_and_noble = False

        # only used if requires a full refresh of all data
        self.force_cr_for_details = False
        self.refresh_volume_details = False
        self.refresh_series_data = False

    def parse_volume(self, display_name: str, category: str):
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

    def scrape_page(self, item, all_volumes, all_series, all_shop):
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
        self.logger.info('---------- Scraping item... %s | %s ----------', isbn, cr_attr['name'])

        is_new_volume = isbn not in all_volumes
        if (self.query_isbn_db and not is_new_volume) or is_new_volume:
            isbn_results = self.scrape_isbn.isbn_search(isbn)
        else:
            vol_for_isbn = all_volumes[isbn]
            isbn_results = {
                'details': {
                    'release_date': vol_for_isbn['release_date'],
                    'publisher': vol_for_isbn['publisher'],
                    'format': vol_for_isbn['format'],
                    'pages': vol_for_isbn['pages'],
                    'authors': vol_for_isbn['authors'],
                    'isbn_10': vol_for_isbn['isbn_10']
                },
                'shops': all_shop[isbn]['shops'][1:]
            }
            self.logger.info('Volume exists, ISBN search skipped... %s', isbn_results)

        retail_price = max([
            price.attrs['content']
            for price in
            item.find('div', {'class': 'price'}) \
                .find_all('span', {'class': 'value'})
        ])
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']

        volume_number = self.parse_volume(cr_attr['name'], cr_attr['category'])

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
                    'record_updated_date': str(datetime.now()),
                    'coupon': cr_attr['coupon'],
                    'is_on_sale': item.find('div', {'class': 'sale'}) is not None
                },
                *isbn_results['shops']
            ]
        }
        # get barnes and noble data
        if self.query_barnes_and_noble:
            try:
                bn_data = self.scrape_barnes_and_noble.get_barnes_and_noble_data(isbn,
                    [] if is_new_volume else all_shop[isbn]['shops'])
                self.logger.info('Barnes & Noble data: %s', json.dumps(bn_data))
                product['shops'].append(bn_data)
            except (requests.exceptions.RequestException, IndexError):
                self.logger.error('Could not get Barnes & Noble data for %s... ending process',
                                  isbn)
                self.logger.error(traceback.format_exc())
        all_shop[isbn] = product
        self.logger.info('All shop details added: %s', json.dumps(product))

        # get the series data
        brand_name = cr_attr['brand']
        # query series if volume is new ----------- or series is not in data
        if not self.refresh_series_data and isbn in all_volumes \
            and all_volumes[isbn]['series_id'] in all_series:
            #  \
            # and all_volumes[isbn]['series_id'] in all_series:
            self.logger.info('Series found in data... using that instead: %s %s',
                        brand_name, all_volumes[isbn]['series_id'])
            series_details = all_series[all_volumes[isbn]['series_id']]
        elif is_new_volume or self.refresh_series_data:
            self.logger.info('Series not found in data or forcefully updating series...' +
                        ' searching for series ID: %s', brand_name)
            series_details = self.series_search.search_series(brand_name, cr_attr['category'],
                                                              cr_attr['name'])
        else:
            self.logger.info('Skipping series search on existing volume: %s', isbn)
            series_details = { 'series_id': None, 'title': cr_attr['brand'] }
        self.logger.info('Series details: %s', json.dumps(series_details))
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

        # remove description check later?
        fetch_cr_data = (is_new_volume or 'description' not in all_volumes[isbn])
        if fetch_cr_data \
            or (self.refresh_volume_details \
                and (self.query_cr_for_details or self.force_cr_for_details)):
            volume['cover_images'] = [{ 'name': 'primary', 'url': cover_image }]
            # fetch data for description and more images
            self.logger.info('Scraping CR page for description and more cover images: %s', isbn)
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
            self.logger.info('All images: %s for %s', json.dumps(all_images), cr_attr['name'])
            volume['cover_images'].extend(
                [
                    { 'name': 'thumbnail', 'url': img } for img in all_images
                    if img is not cover_image # will not catch because they are thumbnails now
                ]
            )
            all_volumes[isbn] = volume
        # override existing volume details with new volume details
        elif self.refresh_volume_details:
            volume['series_id'] = all_volumes[isbn]['series_id']
            all_volumes[isbn] = volume
            self.logger.info('Volume details refreshed: %s', json.dumps(volume))
        else:
            self.logger.info('Volume exists, not refreshing volume details...')
        self.logger.info('Volume details added: %s', json.dumps(volume))

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
                self.logger.info('Added series to data: %s', series_id)
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
                                float(x['volume'].split('-')[0])
                                if '-' in x['volume']
                                else float(x['volume'])
                            )
                        )
                    )
                    all_series[series_id]['volumes'] = series_volumes
                    self.logger.info('Series exists, added volume: %s to %s', isbn,
                                json.dumps(all_series[series_id]['volumes']))
                else:
                    idx = existing_volumes.index(series_volume['isbn'])
                    all_series[series_id]['volumes'][idx] = series_volume
                    self.logger.info('Series exists, updated volume: %s to %s', isbn,
                                json.dumps(all_series[series_id]['volumes']))
                if self.refresh_series_data:
                    all_series[series_id] = { **all_series[series_id], **series_details }
                    self.logger.info('Series details forcefully updated: %s',
                                json.dumps(all_series[series_id]))

        # broadcast the new data
        websockets.broadcast(CONNECTIONS, json.dumps({
            'volume': all_volumes[isbn],
            'series': all_series[series_id],
            'shop': all_shop[isbn]
        }))

        return all_volumes, all_series, all_shop

    def run_scraper(self):
        '''
        Run the scraper to scrape the Crunchyroll store website for manga volumes
        and series information.
        '''

        start = 11000
        end = 100000000000

        if self.enable_scrape:
            volumes_data = self.data.get_volumes_data()
            series_data = self.data.get_series_data()
            shop_data = self.data.get_shop_data()

            page_base_url = \
                'https://store.crunchyroll.com/collections/manga-books/?cgid=manga-books&srule=New-to-Old'
            category_query = '&prefn1=subcategory&prefv1=Novels|Manhwa|Manhua|Light%20Novels|Manga'
            page_url = page_base_url + category_query

            self.logger.info('Calling: %s&start=%s&sz=100', page_url, start)
            first_soup = BeautifulSoup(
                requests.get(page_url + f'&start={start}&sz=100', timeout=30).text,
                'html.parser'
            )
            cr_total_count = int(first_soup.find('div', {'class': 'pagination-text'})
                              .attrs['data-totalcount'])
            total_count = min(cr_total_count, end) - start
            total_pages = math.ceil(total_count / 100)
            start_page = math.floor(start / 100)
            end_page = math.ceil(min(cr_total_count, end) / 100)
            completed = 0
            self.logger.info('pages to scrape: %s', str(total_pages))

            if self.scrape_all_pages:

                for i in range(start_page, end_page):

                    cancel_scraping = not self.local_dao \
                        .open_file(FilePathEnum.EDITING.value[self.host.value]).get('editing')
                    if start > end or cancel_scraping:
                        self.logger.info('Reached end of pages... %s', str(start - 100))
                        self.local_dao.save_file(FilePathEnum.EDITING.value[self.host.value],
                                                 {"editing": True})
                        break

                    if completed == 0:
                        next_soup = first_soup
                    else:
                        self.logger.info('Calling: %s&start=%s&sz=100', page_url, start)
                        next_soup = BeautifulSoup(
                            requests.get(page_url + f'&start={start}&sz=100', timeout=30).text,
                            'html.parser'
                        )

                    for item in next_soup.find_all('div', {'class': 'product'}):
                        self.logger.info('Starting item %s from page %s of %s',
                                    json.loads(item.attrs['data-gtmdata'])['id'], i, end_page)

                        try:
                            volumes_data, series_data, shop_data \
                                = self.scrape_page(item, volumes_data, series_data, shop_data)

                            # save each volume to file
                            self.data.save_all_files(volumes_data, series_data, shop_data)
                        except Exception:
                            self.logger.error('Error scraping item... skipping...')
                            self.logger.error(traceback.format_exc())
                            continue

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

                    start += 100

        self.logger.info('Finished scraping...')
        print()
