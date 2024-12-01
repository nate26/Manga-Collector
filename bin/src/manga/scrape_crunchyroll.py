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

from concurrent.futures import ThreadPoolExecutor
import json
import math
import re
from datetime import datetime
import traceback
from typing import Any, List
import requests
from bs4 import BeautifulSoup

from src.database.manga_server import MangaServer
from src.enums.host_enum import HostEnum
from src.manga.scrape_isbn import ScrapeISBN
from src.manga.series_search import SeriesSearch
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


    def get_volume_data(self, curr_volume, curr_series, cr_attr, soup_volume, volume_number,
                        cover_image, series_id, isbn_results, is_bundle):
        title = self.get_attr(curr_series, 'title')
        volume = {
            'isbn': cr_attr['id'],
            'brand': cr_attr['brand'],
            'series': title,
            'series_id': series_id,
            'display_name': cr_attr['name'],
            'name': title or cr_attr['brand'], #fix?
            'category': cr_attr['category'],
            'volume': volume_number,
            'url': cr_attr['url'],
            'is_bundle': is_bundle,
            'cover_images': [],
            **(isbn_results or { 'details': {} })['details']
        }

        if soup_volume is not None:
            volume['primary_cover_image'] = cover_image
            # get the release date
            preorder_soup = soup_volume.find('div', {'class': 'pre-order-street-date'})
            if preorder_soup is not None:
                preorder_text = preorder_soup.text
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
            return volume
        # override existing volume details with new volume details
        elif self.refresh_volume_details:
            self.logger.info('Volume details refreshed: %s', json.dumps(volume))
            return volume
        # only update series_id if it is different
        elif series_id != self.get_attr(curr_volume, 'series_id'):
            self.logger.info('Series ID updated on volume: %s | %s', cr_attr['id'], series_id)
            return { 'series_id': series_id }
        return None


    def set_volume(self, curr_volume, curr_series, cr_attr, soup_volume, volume_number,
                   cover_image, series_id, isbn_results, is_bundle):
        # get volume changes
        volume_update = self.get_volume_data(curr_volume, curr_series, cr_attr, soup_volume,
                                             volume_number, cover_image, series_id, isbn_results,
                                             is_bundle)
        #* SET volume data
        if volume_update is not None:
            if curr_volume is not None:
                self.manga_server.update_item('volume', cr_attr['id'], volume_update)
                self.logger.info('Volume updated: %s', json.dumps(volume_update))
            else:
                self.manga_server.create_item('volume', volume_update)
                self.logger.info('Volume created: %s', json.dumps(volume_update))
        else:
            self.logger.info('Volume exists, not refreshing volume details...')


    def update_series_volumes(self, curr_series, isbn) -> List[dict[str, str]]:
        if isbn not in curr_series['volumes']:
            # ? maybe do this sorting someday, but for now we can do it in elixir
            # series_volumes = sorted(
            #     [
            #         *curr_series['volumes'],
            #         series_volume
            #     ],
            #     key = lambda x: (
            #         x['category'],
            #         -1
            #         if x['volume'] is None
            #         else (
            #             float(x['volume'].split('-')[0])
            #             if '-' in x['volume']
            #             else float(x['volume'])
            #         )
            #     )
            # )
            self.logger.info('Volume added in series: %s to %s',
                             isbn,
                             json.dumps(curr_series['volumes']))
            return [ *curr_series['volumes'], isbn ]
        return curr_series['volumes']


    def set_series(self, curr_volume, cr_attr) -> dict[str, Any] | None:
        curr_series = None
        if curr_volume is not None and curr_volume['series_id'] is not None:
            curr_series = self.manga_server.get_item('series', curr_volume['series_id'])

        if curr_series is not None:
            curr_series['volumes'] = self.update_series_volumes(curr_series, cr_attr['id'])
            self.logger.info('Series found in data...: %s %s',
                             curr_series['title'], curr_series['series_id'])
            self.manga_server.update_item('series', curr_volume['series_id'], curr_series)
            self.logger.info('series details updated in DB: %s', json.dumps(curr_series))
            return curr_series

        if curr_volume is None or self.refresh_series_data:
            self.logger.info('Series not found in data or forcefully updating series...' +
                             ' searching for series ID: %s', cr_attr['brand'])
            new_series = {
                **self.series_search.search_series(cr_attr['brand'],
                                                   cr_attr['category'],
                                                   cr_attr['name']),
                'volumes': [cr_attr['id']]
            }
            if curr_volume is None or curr_volume['series_id'] is None:
                curr_series = self.manga_server.get_item('series', new_series['series_id'])

            if curr_series is not None:
                new_series['volumes'] = self.update_series_volumes(curr_series, cr_attr['id'])
                self.manga_server.update_item('series', new_series['series_id'], new_series)
                self.logger.info('series getting refreshed, but maintaining volumes: %s',
                                 json.dumps(new_series))
                return new_series

            if new_series['series_id'] is not None:
                self.manga_server.create_item('series', new_series)
                self.logger.info('series details added to DB: %s', json.dumps(new_series))
                return new_series

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
        if curr_market is not None:
            self.manga_server.update_item('market', isbn, market)
            self.logger.info('market details updated in DB: %s', json.dumps(market))
        else:
            self.manga_server.create_item('market', market)
            self.logger.info('market details added to DB: %s', json.dumps(market))


    def set_shops_data(self, item, cr_attr, isbn: str, isbn_results, is_bundle: bool):
        '''
        Sets the shop data for the given item.

        Parameters:
        - item (dict): The Beautiful soup object for an item in the Crunchyroll store website.
        - cr_attr (dict): The attributes of the item from Crunchyroll.
        - isbn (str): The ISBN of the item.
        - isbn_results (dict): The results of the ISBN search.
        '''
        promotion_text: str = item.find('div', {'class': 'plp-promotion'}).text
        promotion = ''
        promotion_percentage = None
        if promotion_text is not None:
            fpromotion_text = promotion_text.replace('\n', '').strip()
            promotion = fpromotion_text.split('| ')[1] \
                if '| ' in fpromotion_text \
                    else fpromotion_text or ''
            promotion_percentage = float(fpromotion_text.split('%')[0]) \
                if '%' in fpromotion_text \
                    else None

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
                'promotion': promotion,
                'promotion_percentage': promotion_percentage,
                'backorder_details': item.find('div', {'class': 'back-order'}).text,
                'is_bundle': is_bundle,
                'dropped_check': False
            },
            *[
                {
                    **shop,
                    'is_bundle': is_bundle
                }
                for shop in (isbn_results['shops'] if isbn_results is not None else [])
            ]
        ]
        for shop in shops:
            curr_shop = self.manga_server.get_item('shop', shop['item_id'])
            stock_status = cr_attr['Inventory_Status']
            shop['last_stock_update'] = curr_shop['last_stock_update'] \
                if curr_shop is not None and stock_status != curr_shop['stock_status'] \
                else str(datetime.now()) #! TODO update all datetime to correct date format...
            #* save to DB
            if curr_shop is not None:
                self.manga_server.update_item('shop', shop['item_id'], shop)
                self.logger.info('shop details updated in DB: %s', json.dumps(shops))
            else:
                self.manga_server.create_item('shop', shop)
                self.logger.info('shop details added to DB: %s', json.dumps(shops))


    def set_bundle_data(self, is_bundle, curr_bundle, isbn, series_id, cover_image,
                        soup_volume: BeautifulSoup | None):
        if not is_bundle:
            return
        bundle_type = 'Bundle' if 'BUNDLE' in isbn else 'Box Set'
        if curr_bundle is not None and not self.refresh_volume_details:
            self.logger.info('Bundle exists, refreshing basic bundle details...')
            bundle = {
                'item_id': isbn,
                'series_id': series_id,
                'shop_id': isbn + 'CrunchyrollNew',
                'primary_cover_image': cover_image,
                'type': bundle_type
            }
            self.manga_server.update_item('bundle', isbn, bundle)
            self.logger.info('Bundle details updated in DB: %s', json.dumps(bundle))
        else:
            bundle = {
                'item_id': isbn,
                'series_id': series_id,
                'shop_id': isbn + 'CrunchyrollNew',
                'primary_cover_image': cover_image,
                'volumes': [],
                'volume_start': None,
                'volume_end': None,
                'type': bundle_type
            }
            if bundle_type == 'Bundle' and soup_volume is not None:
                vols = soup_volume.find('div', {'class': 'short-description'}).find_all('a')
                volumes_partial = [
                    {
                        'isbn': vol.attrs['href'].split('-')[-1][:-5],
                        'display_name': vol.text,
                        'url': vol.attrs['href']
                    }
                    for vol in vols
                ]
                bundle['volumes'] = [
                    {
                        **vol,
                        'primary_cover_image': soup_volume.find(
                            'div',
                            { 'id': 'pdpCarousel-' + vol["isbn"] }
                        ).find('img').attrs['src']
                    }
                    for vol in volumes_partial
                ]
                volume_numbers = [
                    v for v in [
                        self.parse_volume(vol['display_name'], '')
                        for vol in bundle['volumes']
                    ]
                    if v is not None
                ]
                bundle['volume_start'] = min(volume_numbers)
                bundle['volume_end'] = max(volume_numbers)
            elif soup_volume is not None:
                description = soup_volume.find('div', {'class': 'short-description'}).text
                vol_range = description.split('contains volumes ')[1].split(' ')[0] \
                    .split('-')
                bundle['volume_start'] = vol_range[0]
                bundle['volume_end'] = vol_range[1]
                # TODO once we have a way to query volume by number, we can auto populate volumes

            if curr_bundle is None:
                self.manga_server.create_item('bundle', bundle)
                self.logger.info('Bundle details added to DB: %s', json.dumps(bundle))
            else:
                self.manga_server.update_item('bundle', isbn, bundle)
                self.logger.info('Bundle details updated in DB: %s', json.dumps(bundle))


    def get_isbn_results(self, isbn: str, curr_volume):
        if (self.query_isbn_db and curr_volume is not None) or curr_volume is None:
            return self.scrape_isbn.isbn_search(isbn)
        else:
            self.logger.info('Volume exists, ISBN search skipped...')
            return None


    def get_volume_detail_soup(self, cr_attr, curr_volume, curr_bundle):
        # remove description check later?
        fetch_cr_data_for_vol = (curr_volume is None or \
                         (curr_volume is not None and 'description' not in curr_volume))
        fetch_cr_data_for_bundle = curr_bundle is None
        force_cr_fetch = self.refresh_volume_details and \
            (self.query_cr_for_details or self.force_cr_for_details)
        if fetch_cr_data_for_vol or fetch_cr_data_for_bundle or force_cr_fetch:
            # fetch data for description and more images
            self.logger.info('Scraping CR page for description and more cover images: %s', cr_attr['id'])
            return BeautifulSoup(
                requests.get(cr_attr['url'], timeout=30).text,
                'html.parser'
            )
        return None


    def get_attr(self, item: Any | None, attr):
        return item[attr] if item is not None else None


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

        # ? batch 1: get vol / bundle data
        with ThreadPoolExecutor() as executor1:
            curr_volume, curr_bundle = executor1.map(lambda x: x.result(), [
                executor1.submit(self.manga_server.get_item, 'volume', isbn),
                executor1.submit(self.manga_server.get_item, 'bundle', isbn)
            ])

        # ? batch 2: set market / series, isbn results, volume details
        with ThreadPoolExecutor() as executor2:
            _, curr_series, isbn_results, soup_volume = executor2.map(lambda x: x.result(), [
                executor2.submit(self.set_market_data, item, isbn),
                executor2.submit(self.set_series, curr_volume, cr_attr),
                executor2.submit(self.get_isbn_results, isbn, curr_volume),
                executor2.submit(self.get_volume_detail_soup, cr_attr, curr_volume, curr_bundle)
            ])

        series_id = self.get_attr(curr_series, 'series_id')
        is_bundle = 'BUNDLE' in isbn or 'Box Set' in cr_attr['name']
        cover_image = item.find('img', {'class': 'tile-image'}).attrs['src']
        volume_number = self.parse_volume(cr_attr['name'], cr_attr['category'])

        # ? batch 3: set bundle / shops / volume
        with ThreadPoolExecutor() as executor3:
            executor3.map(lambda x: x.result(), [
                executor3.submit(self.set_bundle_data, is_bundle, curr_bundle, isbn, series_id,
                                 cover_image, soup_volume),
                executor3.submit(self.set_shops_data, item, cr_attr, isbn, isbn_results, is_bundle),
                executor3.submit(self.set_volume, curr_volume, curr_series, cr_attr, soup_volume,
                                 volume_number, cover_image, series_id, isbn_results, is_bundle)
            ])

        self.logger.info('---------- Finished scraping item... %s ----------', isbn)


    def process_item(self, item, page_num, end_page):
        self.logger.info('Starting item %s from page %s of %s',
                         json.loads(item.attrs['data-gtmdata'])['id'],
                         page_num, end_page)
        try:
            self.scrape_page(item)
        except Exception:
            self.logger.error('Error scraping item... skipping...')
            self.logger.error(traceback.format_exc())


    def run_scraper(self):
        '''
        Run the scraper to scrape the Crunchyroll store website for manga volumes
        and series information.
        '''

        if not self.enable_scrape:
            self.logger.info('Scraping is disabled... exiting...')
            return

        start = 0
        end = 10000000000

        # volumes_data = self.data.get_volumes_data()
        # series_data = self.data.get_series_data()
        # shop_data = self.data.get_shop_data()

        page_base_url = 'https://store.crunchyroll.com/collections/manga-books/' + \
            '?cgid=manga-books&srule=New-to-Old'
        category_query = '&prefn1=subcategory&prefv1=Novels|Manhwa|Manhua|Light%20Novels|Manga|Bundles'
        page_url = page_base_url + category_query

        self.logger.info('Calling: %s&start=%s&sz=100', page_url, start)
        first_soup = BeautifulSoup(
            requests.get(page_url + f'&start={start}&sz=100', timeout=30).text,
            'html.parser'
        )
        cr_total_count = float(first_soup.find('div', {'class': 'pagination-text'})
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

            items = next_soup.find_all('div', {'class': 'product'})
            thread_count = 3 if i == 0 else 20
            with ThreadPoolExecutor(thread_count) as executor3:
                res = executor3.map(lambda x: x.result(), [
                    executor3.submit(self.process_item, item, i, end_page)
                    for item in items
                ])
            completed += 1
            print('completed: ' + str(completed) + ' | total: ' + str(end_page), end='\r')

                # update progress bar
                # progress = round((completed / total_count) * 50)
                # remaining = 50 - progress
                # percentage = round((completed / total_count) * 100, ndigits=2)
                # print('progress: |' + ''
                #         .join(['=' for _ in range(progress)]) + ''
                #         .join(['-' for _ in range(remaining)]) +
                #         '| ' + str(percentage) + '%',
                #         end='\r')

            start += 100

        self.logger.info('Finished scraping...')
