'''GQL Mutations to modify data in the DB'''

import json
from typing import List
import requests
from src.enums.host_enum import HostEnum
from src.data import Data
from src.interfaces.icollection import ICollection
from src.util.manga_logger import MangaLogger

class Mutations:
    '''
    A class used to modify data in the data layer
    
    ...
    
    Attributes
    ----------
    - host: HostEnum
        The host machine to know where to access data for logging
    
    Methods
    -------
    - create_volume_resolver(_obj, _info, volume_input: Dict)
        Create a new volume record in the DB
    - update_volume_resolver(_obj, _info, isbn: str, volume_update: Dict)
        Update an existing volume record in the DB
    - delete_volume_resolver(_obj, _info, isbn: str)
        Delete an existing volume record in the DB
    '''

    def __init__(self, host: HostEnum, data: Data) -> None:
        self.data = data
        self.logger = MangaLogger(host).register_logger(__name__)

    def update_volume_resolver(self, _obj, _info, user_id: str, volume_update: List[ICollection]):
        '''
        Update an existing volume record in the DB
        '''
        try:
            response = self.data.add_to_collection_data(user_id, volume_update)
            payload = {
                'success': True,
                'record': response
            }
        except requests.exceptions.RequestException as e:
            payload = {
                'success': False,
                'errors': ['Could not complete AWS request' + e]
            }
        except ValueError as e:
            payload = {
                'success': False,
                'errors': ['Incorrect volume record format provided... ' + e
                           + ' --- ' + json.dumps(volume_update)]
            }
        return payload

    def delete_collection_records_resolver(self, _obj, _info, isbn: str):
        '''
        Delete an existing volume record in the DB
        '''
        try:
            volume_data = self.data.get_volumes_data()
            if isbn in volume_data:
                # db.session.delete(manga_record)
                # db.session.commit()
                payload = {
                    'success': True
                }
            else:
                payload = {
                    'success': False,
                    'errors': ['Volume Record by ID ' + isbn + ' does not exist...']
                }
        except ValueError:  # date format errors
            payload = {
                'success': False,
                'errors': ['Could not delete volume record by ID ' + isbn]
            }
        return payload
