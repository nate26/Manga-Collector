"""Adapter for connecting to AWS Graphql API"""

from datetime import datetime, timedelta
from typing import Any, List
import uuid
import requests
from src.interfaces.icollection import ICollection
from src.interfaces.iwishlist import IWishlist
from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class AWSAdapter:
    """Adapter for connecting to AWS Graphql API"""

    def __init__(self, host: HostEnum) -> None:
        self.logger = MangaLogger(host).register_logger(__name__)
        vault = LocalDAO(host).open_file(FilePathEnum.VAULT.value[host.value])
        self.collection_host = vault['aws_collection_host']
        self.collection_api_key = vault['aws_collection_api_key']
        self.user_list_host = vault['aws_user_list_host']
        self.user_list_api_key = vault['aws_user_list_api_key']

    #region Collection

    def __call_collection_gql(self, graphql: str, variables: dict | None = None
                              ) -> requests.Response:
        start = datetime.now()
        response = requests.post(
            url = 'https://' + self.collection_host + '/graphql',
            json = {
                'query': graphql,
                'variables': variables or {}
            },
            headers = {
                'Content-type': 'application/graphql',
                'x-api-key': self.collection_api_key,
                'host': self.collection_host
            },
            timeout=30
        )
        end = (datetime.now() - start).total_seconds()
        self.logger.info('Time to call collection data from AWS: %s', str(timedelta(seconds=end)))
        if 'errors' in response.json():
            self.logger.error(response.json()['errors'])
        return response

    def get_collection_data(self, user_id: str) -> List[ICollection]:
        """
        Gets the collection data from the AWS directory
        """
        graphql_query = """query listMangaUserCollections {
            listMangaUserCollections(filter: { user_id: { eq: "%s" } }) {
                items {
                    id
                    user_id
                    cost
                    giftToMe
                    purchaseDate
                    isbn
                    merchant
                    read
                    tags
                    state
                    inserted
                    updated
                }
            }
        }""" % user_id
        response = self.__call_collection_gql(graphql_query)
        return response.json()['data']['listMangaUserCollections']['items']

    def get_single_collection_item(self, vol_id: str, user_id: str) -> ICollection:
        """
        Gets a single collection item by id from the AWS directory.
        """
        graphql_query = """query getMangaUserCollection {
            getMangaUserCollection(id: "%s", user_id: "%s") {
                id
                user_id
                cost
                giftToMe
                purchaseDate
                isbn
                merchant
                read
                tags
                state
                inserted
                updated
            }
        }""" % (vol_id, user_id)
        print(graphql_query)
        response = self.__call_collection_gql(graphql_query)
        return response.json()['data']['getMangaUserCollection']

    def save_collection_item(self, save_items: List[ICollection]) -> List[Any]:
        """
        Saves a list of items to the collection data.
        If the item has an id, it will update the item. If it does not, it will create a new item.

        Returns
        -------
        List[Any]
            A list of the results from the AWS call
        """
        results = []
        for save_item in save_items:
            graphql_mutation = """mutation save_coll($input: UpdateMangaUserCollectionInput!) {
                updateMangaUserCollection(input: $input) {
                    id
                    user_id
                    cost
                    giftToMe
                    purchaseDate
                    isbn
                    merchant
                    read
                    tags
                    state
                    inserted
                    updated
                }
            }"""
            if 'id' not in save_item:
                save_item['id'] = str(uuid.uuid4())
                save_item['inserted'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                del save_item['temp_id']
                graphql_mutation = """mutation save_coll($input: CreateMangaUserCollectionInput!) {
                    createMangaUserCollection(input: $input) {
                        id
                        user_id
                        cost
                        giftToMe
                        purchaseDate
                        isbn
                        merchant
                        read
                        tags
                        state
                        inserted
                        updated
                    }
                }"""
            save_item['updated'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            result = self.__call_collection_gql(graphql_mutation, { 'input': save_item })
            results.append(result.json())
        return results

    def delete_collection_item(self, ids: List[str], user_id: str) -> List[Any]:
        """
        Deletes a list of items from the user list data by the provided ids.

        Returns
        -------
        List[Any]
            A list of the results from the AWS call
        """
        results = []
        for vol_id in ids:
            graphql_mutation = ("""mutation deleteMangaUserCollection {
                deleteMangaUserCollection(input: {id: "%s", user_id: "%s"}) {
                    id
                    user_id
                }
            }""") % (vol_id, user_id)
            result = self.__call_collection_gql(graphql_mutation)
            results.append(result.json())
        return results

    #endregion

    #region User List

    def __call_user_list_gql(self, graphql: str, variables: dict | None = None
                             ) -> requests.Response:
        start = datetime.now()
        response = requests.post(
            url = 'https://' + self.user_list_host + '/graphql',
            json = {
                'query': graphql,
                'variables': variables or {}
            },
            headers = {
                'Content-type': 'application/graphql',
                'x-api-key': self.user_list_api_key,
                'host': self.user_list_host
            },
            timeout=30
        )
        end = (datetime.now() - start).total_seconds()
        self.logger.info('Time to call user list data from AWS: %s', str(timedelta(seconds=end)))
        if 'errors' in response.json():
            self.logger.error(response.json()['errors'])
        return response

    def get_user_list_data(self, user_id: str) -> List[IWishlist]:
        """
        Gets the user list data from the AWS directory
        """
        graphql_query = """query listMangaUserLists {
            listMangaUserLists(filter: { user_id: { eq: "%s" } }) {
                items {
                    id
                    user_id
                    inserted
                    isbn
                    planned_purchase_date
                    priority
                    updated
                    user_list
                }
            }
        }""" % user_id
        response = self.__call_user_list_gql(graphql_query)
        return response.json()['data']['listMangaUserLists']['items']

    def get_single_user_list_item(self, vol_id: str, user_id: str) -> IWishlist:
        """
        Gets a single user list item by id from the AWS directory.
        """
        graphql_query = """query getMangaUserLists {
            getMangaUserLists(id: "%s", user_id: "%s") {
                id
                user_id
                inserted
                isbn
                planned_purchase_date
                priority
                updated
                user_list
            }
        }""" % (vol_id, user_id)
        print(graphql_query)
        response = self.__call_user_list_gql(graphql_query)
        return response.json()['data']['getMangaUserLists']

    def save_user_list_item(self, save_items: List[IWishlist]) -> List[Any]:
        """
        Saves a list of items to the user list data.
        If the item has an id, it will update the item. If it does not, it will create a new item.

        Returns
        -------
        List[Any]
            A list of the results from the AWS call
        """
        results = []
        for save_item in save_items:
            graphql_mutation = """mutation save_userlist($input: UpdateMangaUserListsInput!) {
                updateMangaUserLists(input: $input) {
                    id
                    inserted
                    isbn
                    planned_purchase_date
                    priority
                    updated
                    user_id
                    user_list
                }
            }"""
            if 'id' not in save_item:
                save_item['id'] = str(uuid.uuid4())
                save_item['inserted'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                graphql_mutation = """mutation save_userlist($input: CreateMangaUserListsInput!) {
                    createMangaUserLists(input: $input) {
                        id
                        inserted
                        isbn
                        planned_purchase_date
                        priority
                        updated
                        user_id
                        user_list
                    }
                }"""
            save_item['updated'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            result = self.__call_user_list_gql(graphql_mutation, { 'input': save_item })
            results.append(result.json())
        return results

    def delete_user_list_item(self, ids: List[str], user_id: str) -> List[Any]:
        """
        Deletes a list of items from the user list data by the provided ids.

        Returns
        -------
        List[Any]
            A list of the results from the AWS call
        """
        results = []
        for vol_id in ids:
            graphql_mutation = ("""mutation deleteMangaUserLists {
                deleteMangaUserLists(input: {id: "%s", user_id: "%s"}) {
                    id
                    user_id
                }
            }""") % (vol_id, user_id)
            result = self.__call_user_list_gql(graphql_mutation)
            results.append(result.json())
        return results
