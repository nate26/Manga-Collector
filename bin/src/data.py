'''Module to get and write to local json files or AWS.'''

import json
from typing import Any, Dict, List

import requests

from src.database.aws_adapter import AWSAdapter
from src.enums.host_enum import HostEnum
from src.enums.file_path_enum import FilePathEnum
from src.interfaces.icollection import ICollection
from src.interfaces.iseries import ISeries
from src.interfaces.ishop import IShop
from src.interfaces.ivolume import IVolume
from src.interfaces.iwishlist import IWishlist
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class Data:
    '''
    A class used to get and write to local json files.

    ...

    Attributes
    ----------
    host : HostEnum
        The the host machine to know where to access data for logging

    Methods
    -------
    get_library_data()
        Gets the data from a json file
    get_series_data()
        Gets the data from a json file
    get_collection_data(user_id=str)
        Gets the data from a json file
    add_to_collection_data(data=Any)
        Writes data to a json file
    delete_from_collection_data(data=Any)
        Writes data to a json file
    get_wishlist_data(user_id=str)
        Gets the data from a json file
    add_to_wishlist_data(data=Any)
        Writes data to a json file
    delete_from_wishlist_data(data=Any)
        Writes data to a json file
    '''

    def __init__(self, host: HostEnum):
        self.host = host
        self.local_dao = LocalDAO(host)
        self.aws_dao = AWSAdapter(host)
        self.logger = MangaLogger(host).register_logger(__name__)

        self.all_collection_data: Dict[str, List[ICollection]] = {}
        self.all_wishlist_data: Dict[str, List[IWishlist]] = {}

    def get_volumes_data(self) -> Dict[str, IVolume]:
        '''
        Gets the volumes data from a json file

        Returns:
        - dict: The volumes data from the given file path.
        '''
        return self.local_dao.open_file(FilePathEnum.VOLUMES.value[self.host.value])

    def get_series_data(self) -> Dict[str, ISeries]:
        '''
        Gets the series data from a json file

        Returns:
        - dict: The series data from the given file path.
        '''
        return self.local_dao.open_file(FilePathEnum.SERIES.value[self.host.value])

    def get_shop_data(self) -> Dict[str, IShop]:
        '''
        Gets the shop data from a json file

        Returns:
        - dict: The shop data from the given file path.
        '''
        return self.local_dao.open_file(FilePathEnum.SHOP.value[self.host.value])

    def get_collection_data(self, user_id: str) -> List[ICollection]:
        '''
        Gets the collection data from AWS

        Parameters:
        - user_id (str): The user id to get the data for.

        Returns:
        - dict: The collection data from the given file path.
        '''
        if user_id in self.all_collection_data:
            return self.all_collection_data[user_id]

        if self.host == HostEnum.MOCK:
            return self.local_dao.open_file('./db/mocks/mock-collection.json')

        collection_data = self.aws_dao.get_collection_data(user_id)

        self.all_collection_data[user_id] = collection_data
        return collection_data

    def add_to_collection_data(self, user_id: str,
                               volumes_update: List[ICollection]) -> List[Any]:
        '''
        Inserts records into the AWS collection data

        Parameters:
        - data (Any): The records to insert.

        Returns:
        - str: The response from the AWS insert operation.
        '''
        self.logger.info(json.dumps(volumes_update))
        if self.host == HostEnum.MOCK:
            return []
        results = self.aws_dao.save_collection_item(volumes_update)
        saved: List[ICollection] = [
            result['data']['createMangaUserCollection']
            if 'createMangaUserCollection' in result['data']
            else result['data']['updateMangaUserCollection']
            for result
            in results
            if 'errors' not in result
        ]

        # update cache
        if user_id in self.all_collection_data:
            for new_record in saved:
                old_record = next(
                    (i for i in self.all_collection_data[user_id] \
                        if i.get('id') == new_record.get('id')),
                    None
                )
                if old_record is not None:
                    self.all_collection_data[user_id].remove(old_record)
                self.all_collection_data[user_id].append(new_record)
        self.logger.info(results)

        if len(saved) != len(volumes_update):
            errors = [error for error in results if 'errors' in error]
            self.logger.error('Some records were not saved')
            self.logger.error(errors)
            raise requests.exceptions.RequestException(errors)
        return saved

    def delete_from_collection_data(self, user_id: str, ids_delete: List[str]) -> List[Any]:
        '''
        Deletes records from AWS collection data

        Parameters:
        - data (Any): The records to delete.

        Returns:
        - str: The text response from the AWS delete operation.
        '''
        self.logger.info(json.dumps(ids_delete))
        if self.host == HostEnum.MOCK:
            return []
        deleted = self.aws_dao.delete_collection_item(ids_delete, user_id)

        # update cache
        if user_id in self.all_collection_data:
            for id_delete in ids_delete:
                old_record = next(
                    (i for i in self.all_collection_data[user_id] \
                        if i.get('id') == id_delete),
                    None
                )
                if old_record is not None:
                    self.all_collection_data[user_id].remove(old_record)
        self.logger.info(deleted)
        return deleted

    def get_wishlist_data(self, user_id: str) -> List[IWishlist]:
        '''
        Gets the wishlist data from AWS

        Parameters:
        - user_id (str): The user id to get the data for.

        Returns:
        - dict: The wishlist data from the given file path.
        '''
        if user_id in self.all_wishlist_data:
            return self.all_wishlist_data[user_id]

        if self.host == HostEnum.MOCK:
            return self.local_dao.open_file('./db/mocks/mock-wishlist.json')

        wishlist_data = self.aws_dao.get_user_list_data(user_id)

        self.all_wishlist_data[user_id] = wishlist_data
        return wishlist_data

    def add_to_wishlist_data(self, user_id: str, list_updates: List[IWishlist]) -> List[Any]:
        '''
        Inserts records into the AWS wishlist data

        Parameters:
        - data (Any): The records to insert.

        Returns:
        - str: The response from the AWS insert operation.
        '''
        self.logger.info(json.dumps(list_updates))
        if self.host == HostEnum.MOCK:
            return []
        return self.aws_dao.save_user_list_item(list_updates)

    def delete_from_wishlist_data(self, user_id: str, ids_delete: List[str]) -> List[Any]:
        '''
        Deletes records from AWS wishlist data

        Parameters:
        - data (Any): The records to delete.

        Returns:
        - str: The text response from the AWS delete operation.
        '''
        self.logger.info(json.dumps(ids_delete))
        if self.host == HostEnum.MOCK:
            return []
        return self.aws_dao.delete_user_list_item(ids_delete, user_id)

    def save_all_files(self, volumes_provided, series_provided, shop_provided):
        '''
        Saves all the given data structures to their respective files via the local dao.

        Parameters:
        - volumes_provided: The volumes data structure to save to the file.
        - series_provided: The series data structure to save to the file.
        - shop_provided: The shop data structure to save to the file.
        '''
        self.local_dao.save_all_files(volumes_provided, series_provided, shop_provided)
