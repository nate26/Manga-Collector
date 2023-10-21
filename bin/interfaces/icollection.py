from interfaces.ilibrary import ILibraryItem

class ICollection(dict):
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

class ICollectionDisplay(ICollection, ILibraryItem):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
