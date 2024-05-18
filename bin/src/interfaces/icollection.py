'''Interface for Collection details of a book'''

class ICollection(dict):
    '''Purchase details and collection details of a book'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    id: str
    user_id: str
    isbn: str
    state: str
    cost: float
    merchant: str
    purchaseDate: str
    giftToMe: bool
    read: bool
    inserted: str
    updated: str
