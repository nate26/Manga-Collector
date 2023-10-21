class IWishlist(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    id: str
    user_id: str
    isbn: str
    user_list: str
    priority: str
    planned_purchase_date: str