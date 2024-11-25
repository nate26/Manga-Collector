'''Module to get and write to local json files or AWS.'''

import traceback
import requests

from src.enums.host_enum import HostEnum
from src.enums.file_path_enum import FilePathEnum
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class MangaServer:

    def __init__(self, host: HostEnum):
        self.host = host
        self.url = FilePathEnum.MANGA_SERVER.value[self.host.value]
        self.local_dao = LocalDAO(host)
        self.logger = MangaLogger(host).register_logger(__name__)

    def get_item(self, item_type: str, id: str):
        try:
            self.logger.info(f'Fetching {item_type}: {id}')
            return requests.get(f'{self.url}/{item_type}/{id}').json()
        except Exception as e:
            self.logger.warning(f'Error getting {item_type}: {e}')
            self.logger.warning(traceback.format_exc())
            return None

    def create_item(self, item_type: str, item: dict):
        try:
            self.logger.info(f'Creating {item_type}: {item}')
            return requests.post(f'{self.url}/{item_type}', { item_type: item }).json()
        except Exception as e:
            self.logger.error(f'Error creating {item_type}: {e}')
            self.logger.error(traceback.format_exc())
            raise e
        
    def update_item(self, item_type: str, id: str, item: dict):
        try:
            self.logger.info(f'Updating {item_type}: {id} > {item}')
            return requests.put(f'{self.url}/{item_type}/{id}', { item_type: item }).json()
        except Exception as e:
            self.logger.error(f'Error updating {item_type}: {e}')
            self.logger.error(traceback.format_exc())
            raise e
    
    def delete_item(self, item_type: str, id: str):
        try:
            self.logger.info(f'Deleting {item_type}: {id}')
            return requests.delete(f'{self.url}/{item_type}/{id}').json()
        except Exception as e:
            self.logger.error(f'Error deleting {item_type}: {e}')
            self.logger.error(traceback.format_exc())
            raise e
