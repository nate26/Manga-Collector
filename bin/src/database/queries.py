'''GQL Queries to get data from the DB'''

import json
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from requests import RequestException
from src.data import Data
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

    def __get_data(self, user_id: str | None):
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
            with ThreadPoolExecutor(6) as executor:
                futures = [
                    executor.submit(self.data.get_volumes_data),
                    executor.submit(self.data.get_series_data),
                    executor.submit(self.data.get_shop_data),
                    executor.submit(self.data.get_collection_data if user_id is not None else lambda x: [], user_id),
                    executor.submit(self.data.get_wishlist_data if user_id is not None else lambda x: [], user_id)
                ]
                return executor.map(lambda x: x.result(), futures)
        except Exception as exc:
            self.logger.error('Failed to get data')
            self.logger.error(traceback.format_exc())
            raise RequestException('Failed to get data') from exc

    def __parse_volume(self, isbn, volume_data, series_data, shop_data, collection_data, wishlist_data):
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
        parsed_volume_data = volume_data[isbn] if isbn in volume_data \
            else {
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
            }
        primary_images = [
            image for image in parsed_volume_data['cover_images'] if image['name'] == 'primary'
        ]
        alt_images = [
            image for image in parsed_volume_data['cover_images'] if image['name'] != 'primary'
        ]
        return {
            **parsed_volume_data,
            'primary_cover_image_url': primary_images[0]['url'] if len(primary_images) > 0 else None,
            'other_images': alt_images,
            'series_data': series_data[parsed_volume_data['series_id']] \
                if parsed_volume_data['series_id'] is not None else {
                    'series_id': '',
                    'url': ''
                },
            'retail_price': shop_data[isbn]['retail_price'] if isbn in shop_data else None,
            'purchase_options': shop_data[isbn]['shops'] if isbn in shop_data else {
                'store': '',
                'url': ''
            },
            'user_collection_data': [entry for entry in collection_data if entry['isbn'] == isbn],
            'user_wishlist_data': [entry for entry in wishlist_data if entry['isbn'] == isbn]
        }

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
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)

            self.logger.info(json.dumps(collection_data, indent=4))
            user_volumes = sorted(
                [
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
                ],
                key = lambda x: (
                    x['name'],
                    x['category'],
                    -1 if x['volume'] is None
                    else (
                        float(x['volume'].split('-')[0])
                        if '-' in x['volume']
                        else float(x['volume'])
                    )
                )
            )

            self.logger.info('Found %s total volumes in user collection', len(user_volumes))
            return {
                'success': True,
                'records': user_volumes
            }
        except RequestException:
            return {
                'success': False,
                'errors': ['could not fetch series data... ' + str(traceback.format_exc())]
            }
