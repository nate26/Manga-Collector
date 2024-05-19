'''GQL Mutations to modify data in the DB'''

import json
from typing import Dict
from flask import jsonify
from src.data import Data
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

    def __init__(self, host) -> None:
        self.data = Data(host)
        self.logger = MangaLogger(host).register_logger(__name__)

    def create_volume_resolver(self, _obj, _info, volume_input: Dict):
        '''
        Create a new volume record in the DB
        '''
        try:
            # db.session.add(volume)
            # db.session.commit()
            payload = {
                'success': True,
                'record': jsonify(volume_input)
            }
        except ValueError:  # date format errors
            payload = {
                'success': False,
                'errors': ['Incorrect volume record format provided ' + json.dumps(volume_input)]
            }
        return payload

    def update_volume_resolver(self, _obj, _info, isbn: str, volume_update: Dict):
        '''
        Update an existing volume record in the DB
        '''
        try:
            volume_data = self.data.get_volumes_data()
            if isbn in volume_data:
                existing = volume_data[isbn]
                for key, val in volume_update.items():
                    setattr(existing, key, val)
                # db.session.add(existing)
                # db.session.commit()
                payload = {
                    'success': True,
                    'record': jsonify(existing)
                }
            else:
                payload = {
                    'success': False,
                    'errors': ['Record by ID ' + isbn + ' does not exist...']
                }
        except ValueError:  # date format errors
            payload = {
                'success': False,
                'errors': ['Incorrect volume record format provided ' + json.dumps(volume_update)]
            }
        return payload

    def delete_volume_resolver(self, _obj, _info, isbn: str):
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
