'''A module for the IShop interface.'''

from typing import List


class IStoreItem:
    '''A class used to represent a store item.'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    store: str
    condition: str
    url: str
    store_price: float
    stock_status: str
    last_stock_update: str
    coupon: str
    is_on_sale: bool

class IShop:
    '''A class used to represent a shop item.'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    isbn: str
    retail_price: float
    shops: List[IStoreItem]
