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

from calendar import c
import json
import math
import re
from datetime import datetime
import traceback
from typing import Any
import requests
from bs4 import BeautifulSoup
import websockets

from run_websocket import CONNECTIONS
from src.database.manga_server import MangaServer
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
        self.manga_server = MangaServer(host)

        self.enable_scrape = True

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
        search_volume = re.search(r' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name)
        if search_volume:
            inner_volume = re.search(r'\d+\.?\-?\d*', search_volume.group(0))
            if inner_volume:
                return inner_volume.group(0)
        
        search_vol = re.search(r' [()]?Vol[a-z]?[()]? \d+\.?\-?\d*', display_name)
        if search_vol:
            inner_vol = re.search(r'\d+\.?\-?\d*', search_vol.group(0))
            if inner_vol:
                return inner_vol.group(0)
        
        search_vol_dot = re.search(r' [()]?Vol.[a-z]?[()]? \d+\.?\-?\d*', display_name)
        if search_vol_dot:
            inner_vol_dot = re.search(r'\d+\.?\-?\d*', search_vol_dot.group(0))
            if inner_vol_dot:
                return inner_vol_dot.group(0)
        
        search_gn = re.search(r' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name)
        if search_gn:
            inner_gn = re.search(r'\d+\.?\-?\d*', search_gn.group(0))
            if inner_gn:
                return inner_gn.group(0)
        
        search_box = re.search(r' [()]?Box Set[()]? \d+\.?\-?\d*', display_name)
        if search_box:
            inner_box = re.search(r'\d+\.?\-?\d*', search_box.group(0))
            if inner_box:
                return inner_box.group(0)
        
        search_any = re.search(r' [()]?' + category + r'[a-z]?[()]? \d+\.?\-?\d*', display_name)
        if search_any:
            inner_any = re.search(r'\d+\.?\-?\d*', search_any.group(0))
            if inner_any:
                return inner_any.group(0)
        
        return None
    

    def get_series(self, curr_volume, cr_attr) -> dict[str, Any] | None:
        curr_series = None
        if curr_volume != None and curr_volume['series_id'] != None:
            curr_series = self.manga_server.get_item('series', curr_volume['series_id'])

        if curr_series != None:
            self.logger.info('Series found in data...: %s %s',
                             curr_series['title'], curr_series['series_id'])
            return curr_series
        elif curr_volume == None or self.refresh_series_data:
            self.logger.info('Series not found in data or forcefully updating series...' +
                             ' searching for series ID: %s', cr_attr['brand'])
            return self.series_search.search_series(cr_attr['brand'],
                                                    cr_attr['category'],
                                                    cr_attr['name'])
        self.logger.info('Skipping series search on existing volume: %s', cr_attr['id'])
        return None


    def set_market_data(self, item, isbn: str):
        '''
        Sets the market data for the given item.

        Parameters:
        - item (dict): The Beautiful soup object for an item in the Crunchyroll store website.
        - isbn (str): The ISBN of the item.
        '''
        retail_price = max([
            price.attrs['content']
            for price in
            item.find('div', {'class': 'price'}) \
                .find_all('span', {'class': 'value'})
        ])
        market = {
            'isbn': isbn,
            'retail_price': float(retail_price)
        }
        curr_market = self.manga_server.get_item('market', isbn)        
        if curr_market != None:
            self.manga_server.update_item('market', isbn, market)
        else:
            self.manga_server.create_item('market', market)
        self.logger.info('market details set: %s', json.dumps(market))

    
    def set_shops_data(self, item, cr_attr, isbn: str, isbn_results, is_bundle: bool):
        '''
        Sets the shop data for the given item.

        Parameters:
        - item (dict): The Beautiful soup object for an item in the Crunchyroll store website.
        - cr_attr (dict): The attributes of the item from Crunchyroll.
        - isbn (str): The ISBN of the item.
        - isbn_results (dict): The results of the ISBN search.
        '''
        promotion_text = item.find('div', {'class': 'plp-promotion'}).text
        shops = [
            {
                'item_id': isbn + 'CrunchyrollNew',
                'isbn': isbn,
                'store': 'Crunchyroll',
                'condition': 'New',
                'url': cr_attr['url'],
                'price': float(cr_attr['price']),
                'stock_status': cr_attr['Inventory_Status'],
                'coupon': cr_attr['coupon'],
                'is_on_sale': item.find('div', {'class': 'sale'}) is not None,
                #! monitor this, may hide if is_on_sale
                'exclusive': item.find('div', {'class': 'exclusive'}) is not None,
                'promotion': promotion_text.split('| ')[1] if promotion_text != None else '',
                'promotion_percentage': float(promotion_text.split('%')[0]) \
                    if promotion_text != None else None,
                'backorder_details': item.find('div', {'class': 'back-order-instock-date'}).text,
                'is_bundle': is_bundle,
                'dropped_check': False
            },
            *[
                {
                    **shop,
                    'is_bundle': is_bundle
                }
                for shop in isbn_results['shops']
            ]
        ]
        for shop in shops:
            curr_shop = self.manga_server.get_item('shop', shop['item_id'])
            stock_status = cr_attr['Inventory_Status']
            shop['last_stock_update'] = curr_shop['last_stock_update'] \
                if curr_shop != None and stock_status != curr_shop['stock_status'] \
                else str(datetime.now()) #! TODO update all datetime to correct date format...
            #* save to DB
            if curr_shop != None:
                self.manga_server.update_item('shop', shop['item_id'], shop)
            else:
                self.manga_server.create_item('shop', shop)
        self.logger.info('shop details set: %s', json.dumps(shops))


    def get_attr(self, item: Any | None, attr):
        return item[attr] if item != None else None


    def scrape_page(self, item):
        '''
        Scrapes the given URL for manga volumes and series,
        and updates the given data structures with the results.

        Parameters:
        - item (dict): The Beautiful soup object for an item in the Crunchyroll store website.
        '''
        # bs4 object to dict
        cr_attr = {
            **json.loads(item.attrs['data-gtmdata']),
            **json.loads(item.find('div', {'class': 'product-tile'}).attrs['data-segmentdata'])
        }
        isbn = cr_attr['id']
        self.logger.info('---------- Scraping item... %s | %s ----------', isbn, cr_attr['name'])

        # current DB data
        curr_volume = self.manga_server.get_item('volume', isbn)

        # isbn search
        isbn_results = None
        is_new_volume = curr_volume != None
        if (self.query_isbn_db and not is_new_volume) or is_new_volume:
            isbn_results = self.scrape_isbn.isbn_search(isbn)
        else:
            self.logger.info('Volume exists, ISBN search skipped...')

        is_bundle = 'BUNDLE' in isbn or 'Box Set' in cr_attr['name']
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']
        brand_name = cr_attr['brand']

        #* SET market data
        self.set_market_data(item, isbn)

        #* SET shop data
        self.set_shops_data(item, cr_attr, isbn, isbn_results, is_bundle)

        curr_series = self.get_series(curr_volume, cr_attr)
        self.logger.info('Series details: %s', json.dumps(curr_series))
        series_id = self.get_attr(curr_series, 'series_id')

        # get the volume
        title = self.get_attr(curr_series, 'title')
        volume = {
            'isbn': isbn,
            'brand': brand_name,
            'series': title,
            'series_id': series_id,
            'display_name': cr_attr['name'],
            'name': title or brand_name, #fix?
            'category': cr_attr['category'],
            'volume': self.parse_volume(cr_attr['name'], cr_attr['category']),
            'url': cr_attr['url'],
            **(isbn_results or {
                'details': {
                    'release_date': self.get_attr(curr_volume, 'release_date'),
                    'publisher': self.get_attr(curr_volume, 'publisher'),
                    'format': self.get_attr(curr_volume, 'format'),
                    'pages': self.get_attr(curr_volume, 'pages'),
                    'authors': self.get_attr(curr_volume, 'authors'),
                    'isbn_10': self.get_attr(curr_volume, 'isbn_10')
                }
            })['details']
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
                if self.refresh_series_data: # TODO check this before refreshing series data (except for additional volumes)
                    all_series[series_id] = { **all_series[series_id], **series_details }
                    self.logger.info('Series details forcefully updated: %s',
                                json.dumps(all_series[series_id]))

        # broadcast the new data
        # websockets.broadcast(CONNECTIONS, json.dumps({
        #     'volume': all_volumes[isbn],
        #     'series': all_series[series_id],
        #     'shop': all_shop[isbn]
        # }))


    def run_scraper(self):
        '''
        Run the scraper to scrape the Crunchyroll store website for manga volumes
        and series information.
        '''

        if not self.enable_scrape:
            self.logger.info('Scraping is disabled... exiting...')
            return

        start = 0
        end = 1

        # volumes_data = self.data.get_volumes_data()
        # series_data = self.data.get_series_data()
        # shop_data = self.data.get_shop_data()

        page_base_url = 'https://store.crunchyroll.com/collections/manga-books/' + \
            '?cgid=manga-books&srule=New-to-Old'
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

        for i in range(start_page, end_page):

            if start > end:
                self.logger.info('Reached end of pages... %s', str(start - 100))
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
                    self.scrape_page(item)
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
