'''Module to get and write to local json files or AWS.'''

from typing import Dict, List
from bin.src.enums.host_enum import HostEnum
from bin.src.enums.file_path_enum import FilePathEnum
from bin.src.interfaces.icollection import ICollection
from bin.src.interfaces.iseries import ISeries
from bin.src.interfaces.ishop import IShop
from bin.src.interfaces.ivolume import IVolume
from bin.src.interfaces.iwishlist import IWishlist
from bin.src.util.aws_dao import AWSDAO
from bin.src.util.local_dao import LocalDAO
from bin.src.util.manga_logger import MangaLogger

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
        self.aws_dao = AWSDAO(host)
        self.local_dao = LocalDAO(host)
        self.collection_url = 'https://syrrzyi0qf.execute-api.us-east-2.amazonaws.com/v1'
        self.wishlist_url = 'https://d60vento0i.execute-api.us-east-2.amazonaws.com/v2'
        self.logger = MangaLogger(host).register_logger(__name__)

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
        if self.host == HostEnum.MOCK:
            return self.local_dao.open_file('./db/mocks/mock-collection.json')
        return self.aws_dao.get_data(self.collection_url + '/user-records?user_id=' + user_id)

    def add_to_collection_data(self, data) -> str:
        '''
        Inserts records into the AWS collection data
        
        Parameters:
        - data (Any): The records to insert.
        
        Returns:
        - str: The response from the AWS insert operation.
        '''
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        return self.aws_dao.post_data(self.collection_url + '/add-records', data)

    def delete_from_collection_data(self, data) -> str:
        '''
        Deletes records from AWS collection data
        
        Parameters:
        - data (Any): The records to delete.
        
        Returns:
        - str: The text response from the AWS delete operation.
        '''
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        return self.aws_dao.post_data(self.collection_url + '/delete-records', data)
    
    def get_wishlist_data(self, user_id: str) -> List[IWishlist]:
        '''
        Gets the wishlist data from AWS
        
        Parameters:
        - user_id (str): The user id to get the data for.
        
        Returns:
        - dict: The wishlist data from the given file path.
        '''
        if self.host == HostEnum.MOCK:
            return self.local_dao.open_file('./db/mocks/mock-wishlist.json')
        return self.aws_dao.get_data(self.wishlist_url + '/user-records?user_id=' + user_id)

    def add_to_wishlist_data(self, data) -> str:
        '''
        Inserts records into the AWS wishlist data
        
        Parameters:
        - data (Any): The records to insert.
        
        Returns:
        - str: The response from the AWS insert operation.
        '''
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        return self.aws_dao.post_data(self.wishlist_url + '/add-records', data)

    def delete_from_wishlist_data(self, data) -> str:
        '''
        Deletes records from AWS wishlist data
        
        Parameters:
        - data (Any): The records to delete.
        
        Returns:
        - str: The text response from the AWS delete operation.
        '''
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        return self.aws_dao.post_data(self.wishlist_url + '/delete-records', data)
