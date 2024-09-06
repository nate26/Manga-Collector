'''GQL Queries to get data from the DB'''

from datetime import datetime, timedelta
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import List

from requests import RequestException
from src.data import Data
from src.interfaces.icollection import ICollection
from src.interfaces.iseries import ISeries
from src.interfaces.ishop import IShop
from src.interfaces.iwishlist import IWishlist
from src.interfaces.ivolume import ICoverImage
from src.interfaces.ivolume_display import IVolumeDisplay
from src.util.manga_logger import MangaLogger

class Queries:
    '''
    A class used to get data from the data layer

    ...

    Attributes
    ----------
    - host: HostEnum
        The host machine to know where to access data for logging

    Methods
    -------
    - get_record_resolver(isbn: str, user_id: str)
        Gets a single record by its ID from the DB
    - all_records_resolver(user_id: str)
        Gets a list of all records from the DB
    '''

    def __init__(self, host) -> None:
        self.data = Data(host)
        self.logger = MangaLogger(host).register_logger(__name__)

    def __get_data(self, user_id: str | None = None):
        '''
        Fetches data from the data layer

        Parameters:
        - user_id: str
            The user ID to fetch data for

        Returns:
        - tuple: The fetched data

        Raises:
        - RequestException: If the request to the data layer fails
        '''
        try:
            start_time = datetime.now()
            with ThreadPoolExecutor(5) as executor:
                futures = [
                    executor.submit(self.data.get_volumes_data),
                    executor.submit(self.data.get_series_data),
                    executor.submit(self.data.get_shop_data)
                ]
                if user_id is not None:
                    futures.append(executor.submit(self.data.get_collection_data, user_id))
                    futures.append(executor.submit(self.data.get_wishlist_data, user_id))
                else:
                    futures.append(executor.submit(lambda: []))
                    futures.append(executor.submit(lambda: []))
                results = executor.map(lambda x: x.result(), futures)
                end_time = (datetime.now() - start_time).total_seconds()
                self.logger.info('Time to get all data: %s', str(timedelta(seconds=end_time)))
                return results
        except Exception as exc:
            self.logger.error('Failed to get data')
            self.logger.error(traceback.format_exc())
            raise RequestException('Failed to get data') from exc

    def __parse_volume(self, isbn: str, volume_data: dict[str, ICollection],
                       series_data: dict[str, ISeries], shop_data: dict[str, IShop],
                       collection_data: List[ICollection],
                       wishlist_data: List[IWishlist]) -> IVolumeDisplay:
        '''
        Parses volume data to include additional fields

        Parameters:
        - volume_data: dict
            The volume data to parse
        - series_data: dict
            The series data to parse
        - shop_data: dict
            The shop data to parse
        - collection_data: dict
            The collection data to parse
        - wishlist_data: dict
            The wishlist data to parse

        Returns:
        - dict: The parsed volume data
        '''
        parsed_volume_data: ICollection = volume_data[isbn] if isbn in volume_data \
            else ICollection({
                'isbn': '',
                'display_name': 'Unknown',
                'name': 'Unknown',
                'category': 'Unknown',
                'volume': '0',
                'cover_images': [],
                'series_id': None,
                'url': '',
                'record_added_date': '',
                'record_updated_date': ''
            })
        primary_images = [
            ICoverImage(image) for image in parsed_volume_data['cover_images']
                if image['name'] == 'primary'
        ]
        alt_images = [
            str(image) for image in parsed_volume_data['cover_images']
                if image['name'] != 'primary'
        ]
        shop_item = shop_data[isbn] if isbn in shop_data else IShop({
            'retail_price': None,
            'shops': []
        })
        return IVolumeDisplay({
            **parsed_volume_data,
            'primary_cover_image_url': primary_images[0]['url'] \
                if len(primary_images) > 0 else None,
            'other_images': alt_images,
            'series_data': series_data[parsed_volume_data['series_id']] \
                if parsed_volume_data['series_id'] is not None else {
                    'series_id': '',
                    'url': ''
                },
            'retail_price': shop_item['retail_price'],
            'purchase_options': shop_item['shops'],
            'user_collection_data': [entry for entry in collection_data if entry['isbn'] == isbn],
            'user_wishlist_data': [entry for entry in wishlist_data if entry['isbn'] == isbn]
        })

    def __volume_sort_parse(self, volume: str | None) -> float:
        return -1 if volume is None else (
            float(volume.split('-')[0])
            if '-' in volume
            else float(volume)
        )

    def get_record_resolver(self, _obj, _info, isbn: str, user_id: str | None):
        '''
        Gets a single record by its ID from the DB

        Parameters:
        - isbn: str
            The ID of the record to fetch
        - user_id: str
            The ID of the user to fetch the record for

        Returns:
        - dict: The fetched record

        Raises:
        - RequestException: If the record does not exist or could not be fetched
        '''
        try:
            start = time.perf_counter()
            self.logger.info('get all data start time: %s', start)
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)
            end = time.perf_counter()
            self.logger.info('get all data end time: %s', end)
            self.logger.info('get all data diff time: %s', end - start)
            payload = {
                'success': True,
                'record': self.__parse_volume(
                    isbn,
                    volume_data,
                    series_data,
                    shop_data,
                    collection_data,
                    wishlist_data
                )
            }
        except RequestException:
            payload = {
                'success': False,
                'errors': ['MangaRecord item matching {id} not found']
            }
        return payload

    def all_records_resolver(self, _obj, _info, user_id: str | None):
        '''
        Gets a list of all records from the DB

        Parameters:
        - user_id: str
            The ID of the user to fetch the records for

        Returns:
        - dict: The fetched records

        Raises:
        - RequestException: If there was an error fetching the records
        '''
        try:
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)
            # this might really need parallelization
            payload = {
                'success': True,
                'records': [self.__parse_volume(
                    isbn,
                    volume_data,
                    series_data,
                    shop_data,
                    collection_data,
                    wishlist_data
                ) for isbn in volume_data]
            }
        except RequestException:
            payload = {
                'success': False,
                'errors': ['could not fetch all manga data... ' + str(traceback.format_exc())]
            }
        return payload

    def get_collection_series_resolver(self, _obj, _info, user_id: str):
        '''
        Gets a list of all series in the user's collection

        Parameters:
        - user_id: str
            The ID of the user to fetch the collection for

        Returns:
        - dict: The fetched series

        Raises:
        - RequestException: If there was an error fetching the series
        '''
        try:
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)
            series_ids = set([
                volume_data[entry['isbn']]['series_id']
                for entry in collection_data
                if entry['isbn'] in volume_data and
                volume_data[entry['isbn']]['series_id'] is not None
            ])
            self.logger.info('Found %s series in user collection', len(series_ids))
            solo_volumes = [
                {
                    'series_id': None,
                    'title': volume_data[entry['isbn']]['name'],
                    'associated_titles': [],
                    'url': volume_data[entry['isbn']]['url'],
                    'category': volume_data[entry['isbn']]['category'],
                    'description': volume_data[entry['isbn']]['description'],
                    'cover_image': volume_data[entry['isbn']]['cover_images'][0]['url'],
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
                    'series_match_confidence': 0,
                    'volumes': [volume_data[entry['isbn']]]
                }
                for entry in collection_data
                if entry['isbn'] in volume_data and
                volume_data[entry['isbn']]['series_id'] is None
            ]
            self.logger.info('Found %s solo volumes in user collection', len(solo_volumes))
            user_series = sorted(
                [
                    {
                        **series_data[series_id],
                        'volumes': [
                            self.__parse_volume(
                                entry['isbn'],
                                volume_data,
                                series_data,
                                shop_data,
                                collection_data,
                                wishlist_data
                            )
                            for entry in series_data[series_id]['volumes']
                        ]
                    }
                    for series_id in series_ids
                ] + solo_volumes,
                key = lambda x: (x['title'])
            )
            self.logger.info('Found %s total series in user collection', len(user_series))
            return {
                'success': True,
                'records': user_series
            }
        except RequestException:
            return {
                'success': False,
                'errors': ['could not fetch series data... ' + str(traceback.format_exc())]
            }

    def get_collection_volume_resolver(self, _obj, _info, user_id: str):
        '''
        Gets a list of all parsed volumes in the user's collection

        Parameters:
        - user_id: str
            The ID of the user to fetch the collection for

        Returns:
        - dict: The fetched volumes
        '''
        try:
            start_time = datetime.now()
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)

            start_time_parse = datetime.now()
            volumes = [
                {
                    **self.__parse_volume(
                        vol['isbn'],
                        volume_data,
                        series_data,
                        shop_data,
                        collection_data,
                        wishlist_data
                    ),
                    'user_collection_data': [vol] # overwrite for individual volume
                }
                for vol in collection_data
            ]
            end_time_parse = (datetime.now() - start_time_parse).total_seconds()
            self.logger.info('Time to parse volumes: %s', str(timedelta(seconds=end_time_parse)))

            start_time_sort = datetime.now()
            user_volumes = sorted(
                volumes,
                key = lambda x: (
                    x['name'],
                    x['category'],
                    self.__volume_sort_parse(x['volume'])
                )
            )
            end_time_sort = (datetime.now() - start_time_sort).total_seconds()
            self.logger.info('Time to sort volumes: %s', str(timedelta(seconds=end_time_sort)))

            self.logger.info('Found %s total volumes in user collection', len(user_volumes))
            end_time = (datetime.now() - start_time).total_seconds()
            self.logger.info('Time to finish query collection volumes: %s',
                             str(timedelta(seconds=end_time)))
            return {
                'success': True,
                'records': user_volumes
            }
        except RequestException:
            return {
                'success': False,
                'errors': ['could not fetch series data... ' + str(traceback.format_exc())]
            }

    def get_on_sale_volumes_resolver(self, _obj, _info):
        '''
        Gets a list of all volumes on sale

        Returns:
        - dict: The fetched volumes
        '''
        try:
            volume_data, _, shop_data, _, _ = self.__get_data()
            on_sale_volumes = []
            for _, shop_vol in enumerate(shop_data.values()):
                for shop_item in shop_vol['shops']:
                    if shop_item['is_on_sale'] and \
                        round(shop_item['store_price']) < round(shop_vol['retail_price']):
                        volume = volume_data[shop_vol['isbn']]
                        primary_cover_images = [
                            image['url'] for image in volume['cover_images']
                            if image['name'] == 'primary'
                        ]
                        on_sale_volumes.append({
                            'isbn': shop_vol['isbn'],
                            'display_name': volume['display_name'],
                            'primary_cover_image_url': primary_cover_images[0] \
                                if len(primary_cover_images) > 0 else None,
                            'retail_price': shop_vol['retail_price'],
                            'store': shop_item['store'],
                            'store_price': shop_item['store_price'],
                            'is_on_sale': shop_item['is_on_sale'],
                            'stock_status': shop_item['stock_status'],
                            'condition': shop_item['condition'],
                            'coupon': shop_item['coupon'],
                            'last_stock_update': shop_item['last_stock_update'],
                            'sale_price': round(
                                (1 - shop_item['store_price'] / shop_vol['retail_price']) * 100
                            ),
                            'url': shop_item['url']
                        })

            self.logger.info('Found %s total volumes on sale', len(on_sale_volumes))
            return {
                'success': True,
                'records': sorted(on_sale_volumes, key = lambda x: x['display_name'])
            }
        except RequestException:
            return {
                'success': False,
                'errors': ['could not fetch sale volume data... ' + str(traceback.format_exc())]
            }
