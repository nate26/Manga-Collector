'''GQL Queries to get data from the DB'''

import traceback

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

    def __get_data(self, user_id: str):
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
            # fetch data (consider parallelizing these calls for performance improvement)
            volume_data = self.data.get_volumes_data()
            series_data = self.data.get_series_data()
            shop_data = self.data.get_shop_data()
            collection_data = self.data.get_collection_data(user_id)
            wishlist_data = self.data.get_wishlist_data(user_id)
            return volume_data, series_data, shop_data, collection_data, wishlist_data
        except Exception as exc:
            self.logger.error('Failed to get data')
            self.logger.error(traceback.format_exc())
            raise RequestException('Failed to get data') from exc

    def __parse_volume(self, volume_data, series_data, shop_data, collection_data, wishlist_data):
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
        primary_images = [
            image for image in volume_data['cover_images'] if image['name'] == 'primary'
        ]
        alt_images = [
            image for image in volume_data['cover_images'] if image['name'] != 'primary'
        ]
        return {
            **volume_data,
            'primary_cover_image_url': primary_images[0] if len(primary_images) > 0 else None,
            'other_images': alt_images,
            'series': series_data,
            'retail_price': shop_data['retail_price'],
            'purchase_options': shop_data['shops'],
            'user_collection_data': collection_data,
            'user_wishlist_data': wishlist_data
        }

    def get_record_resolver(self, _obj, _info, isbn: str, user_id: str):
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
            volume_data, series_data, shop_data, \
                collection_data, wishlist_data = self.__get_data(user_id)
            payload = {
                'success': True,
                'record': self.__parse_volume(
                    volume_data[isbn],
                    series_data[volume_data['series_id']] \
                        if volume_data['series_id'] is not None else None,
                    shop_data[isbn],
                    [entry for entry in collection_data if entry['isbn'] == isbn],
                    [entry for entry in wishlist_data if entry['isbn'] == isbn]
                )
            }
        except RequestException:
            payload = {
                'success': False,
                'errors': ['MangaRecord item matching {id} not found']
            }
        return payload

    def all_records_resolver(self, _obj, _info, user_id: str):
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
                    volume_data[isbn],
                    series_data[volume_data['series_id']] \
                        if volume_data['series_id'] is not None else None,
                    shop_data[isbn],
                    [entry for entry in collection_data if entry['isbn'] == isbn],
                    [entry for entry in wishlist_data if entry['isbn'] == isbn]
                ) for isbn in volume_data]
            }
        except RequestException:
            payload = {
                'success': False,
                'errors': ['could not fetch all manga data... ' + str(traceback.format_exc())]
            }
        return payload
