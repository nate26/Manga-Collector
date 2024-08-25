'''GQL Mutations to modify data in the DB'''

import json
import traceback
from typing import List
from flask import request
import jwt
import requests
from src.enums.host_enum import HostEnum
from src.data import Data
from src.interfaces.icollection import ICollection
from src.util.auth import Auth
from src.util.manga_logger import MangaLogger

class Mutations:
    '''
    A class used to modify data in the data layer

    ...

    Attributes
    ----------
    - host: HostEnum
        The host machine to know where to access data for logging
    - data: Data
        The data layer to interact with the DB, passed for maintaining state of cached user data

    Methods
    -------
    - update_volume_resolver(_obj, _info, user_id: str, volumes_update: List[ICollection])
        Update an existing volume record in the DB
    - delete_collection_records_resolver(_obj, _info, user_id: str, ids_delete: List[str])
        Delete an existing volume record in the DB
    '''

    def __init__(self, host: HostEnum, data: Data) -> None:
        self.data = data
        self.logger = MangaLogger(host).register_logger(__name__)
        self.auth = Auth(host)

    def update_volume_resolver(self, _obj, _info, user_id: str,
                               volumes_update: List[ICollection]):
        '''
        Update an existing volume record in the DB

        Parameters:
        - user_id (str): The user id to authenticate the request
        - volumes_update (List[ICollection]): The list of volume records to update

        Returns:
        - dict: The response payload

        Raises:
        - requests.exceptions.RequestException: Could not complete AWS request
        - ValueError: Incorrect volume record format provided
        - AuthenticationError: User not authorized to perform this action
        '''
        try:
            if self.auth.decode_user(
                str(request.headers.get('X-Authentication-Token')),
                self.auth.secret
            ) is None:
                raise jwt.InvalidTokenError('User not authorized')

            response = self.data.add_to_collection_data(user_id, volumes_update)
            payload = {
                'success': True,
                'response': response
            }
        except requests.exceptions.RequestException as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['Could not complete AWS request' + str(e)]
            }
        except ValueError as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['Incorrect volume record format provided... ' + str(e)
                           + ' --- ' + json.dumps(volumes_update)]
            }
        except jwt.InvalidTokenError as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['User not authorized to perform this action']
            }
        return payload

    def delete_collection_records_resolver(self, _obj, _info, user_id: str,
                                           ids_delete: List[str]):
        '''
        Delete an existing volume record in the DB

        Parameters:
        - user_id (str): The user id to authenticate the request
        - ids_delete (List[str]): The list of volume records to delete

        Returns:
        - dict: The response payload

        Raises:
        - requests.exceptions.RequestException: Could not complete AWS request
        - ValueError: Incorrect id format provided
        - AuthenticationError: User not authorized to perform this action
        '''
        try:
            if self.auth.decode_user(
                str(request.headers.get('X-Authentication-Token')),
                self.auth.secret
            ) is None:
                raise jwt.InvalidTokenError('User not authorized')

            self.data.delete_from_collection_data(user_id, ids_delete)
            payload = {
                'success': True,
                'response': ids_delete
            }
        except requests.exceptions.RequestException as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['Could not complete AWS request' + str(e)]
            }
        except ValueError as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['Incorrect id format provided... ' + str(e)
                           + ' --- ' + json.dumps(ids_delete)]
            }
        except jwt.InvalidTokenError as e:
            self.logger.error(traceback.format_exc())
            payload = {
                'success': False,
                'errors': ['User not authorized to perform this action']
            }
        return payload
