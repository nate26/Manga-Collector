'''Module to interact with the manga server.'''

import traceback
import requests

from src.enums.host_enum import HostEnum
from src.enums.file_path_enum import FilePathEnum
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class MangaServer:
    '''
    A class used to interact with the manga server.
    '''

    def __init__(self, host: HostEnum):
        self.host = host
        self.url = FilePathEnum.MANGA_SERVER.value[self.host.value]
        self.local_dao = LocalDAO(host)
        self.logger = MangaLogger(host).register_logger(__name__)

    def get_item(self, item_type: str, item_id: str):
        '''Gets an item from the database.'''
        try:
            self.logger.info('Fetching %s: %s', item_type, item_id)
            return requests.get(f'{self.url}/{item_type}/{item_id}', timeout=30).json()
        except Exception:
            self.logger.warning('Error getting %s: %s. Either failed or does not exist', item_type, item_id)
            return None

    def create_item(self, item_type: str, item: dict):
        '''Creates an item in the database.'''
        try:
            url = f'{self.url}/{item_type}'
            body = { item_type: item }
            self.logger.info('Creating at %s with %s', url, body)
            return requests.post(url, json=body, timeout=30).json()
        except Exception as e:
            self.logger.error('Error creating %s', item_type)
            self.logger.error(traceback.format_exc())
            raise e

    def update_item(self, item_type: str, item_id: str, item: dict):
        '''Updates an item in the database.'''
        try:
            self.logger.info('Updating %s: %s > %s', item_type, item_id, item)
            return requests.put(f'{self.url}/{item_type}/{item_id}', json={ item_type: item }, timeout=30).json()
        except Exception as e:
            self.logger.error('Error updating %s: %s', item_type, item_id)
            self.logger.error(traceback.format_exc())
            raise e

    def delete_item(self, item_type: str, item_id: str):
        '''Deletes an item from the database.'''
        try:
            self.logger.info('Deleting %s: %s', item_type, item_id)
            return requests.delete(f'{self.url}/{item_type}/{item_id}', timeout=30).json()
        except Exception as e:
            self.logger.error('Error deleting %s: %s', item_type, item_id)
            self.logger.error(traceback.format_exc())
            raise e
