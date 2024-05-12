'''A module for the IShop interface.'''

class IShop:
    '''A class used to represent a shop item.'''

    def __init__(self, obj: dict = None):
        if obj is not None:
            obj = {}
        for key in obj:
            setattr(self, key, obj[key])

    # item status
    stock_status: str = None
    retail_price: float = None
