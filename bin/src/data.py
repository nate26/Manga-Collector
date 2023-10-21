from enums.host_enum import HostEnum
from enums.file_path_enum import FilePathEnum
from interfaces.icollection import ICollection
from interfaces.ilibrary import ILibrary
from interfaces.iseries import ISeries
from interfaces.iwishlist import IWishlist
from typing import Dict, List
from util.aws_dao import AWSDAO
from util.local_dao import LocalDAO
from util.manga_logger import MangaLogger

class Data:
    
    def __init__(self, host):
        self.host = host
        self.aws_dao = AWSDAO(host)
        self.local_dao = LocalDAO(host)
        self.collection_url = 'https://syrrzyi0qf.execute-api.us-east-2.amazonaws.com/v1'
        self.wishlist_url = 'https://d60vento0i.execute-api.us-east-2.amazonaws.com/v2'
        self.logger = MangaLogger(host, __name__)

    def get_library_data(self) -> Dict[str, ILibrary]:
        return self.local_dao.get_json_file(FilePathEnum.ALL_ITEMS.value[self.host.value])

    def get_series_data(self) -> Dict[str, ISeries]:
        return self.local_dao.get_json_file(FilePathEnum.SERIES.value[self.host.value])

    def get_collection_data(self, user_id: str) -> List[ICollection]:
        if self.host == HostEnum.MOCK:
            return self.local_dao.get_json_file('./db/mocks/mock-collection.json')
        else:
            return self.aws_dao.get_data(self.collection_url + '/user-records?user_id=' + user_id)

    def add_to_collection_data(self, data) -> str:
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        else:
            return self.aws_dao.post_data(self.collection_url + '/add-records', data)

    def delete_from_collection_data(self, data) -> str:
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        else:
            return self.aws_dao.post_data(self.collection_url + '/delete-records', data)
    
    def get_wishlist_data(self, user_id: str) -> List[IWishlist]:
        if self.host == HostEnum.MOCK:
            return self.local_dao.get_json_file('./db/mocks/mock-wishlist.json')
        else:
            return self.aws_dao.get_data(self.wishlist_url + '/user-records?user_id=' + user_id)

    def add_to_wishlist_data(self, data) -> str:
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        else:
            return self.aws_dao.post_data(self.wishlist_url + '/add-records', data)

    def delete_from_wishlist_data(self, data) -> str:
        if self.host == HostEnum.MOCK:
            return 'mock data -- no update made'
        else:
            return self.aws_dao.post_data(self.wishlist_url + '/delete-records', data)
