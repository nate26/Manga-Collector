'''A module for the IShop interface.'''

from typing import List


class IStoreItem(dict):
    '''A class used to represent a store item.'''
    store: str
    condition: str
    url: str
    store_price: float
    stock_status: str
    last_stock_update: str
    coupon: str
    is_on_sale: bool

class IShop(dict):
    '''A class used to represent a shop item.'''
    isbn: str
    retail_price: float
    shops: List[IStoreItem]
