from typing import Dict, List

class ICoverImage(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    name: str
    url: str

class IPromoSale(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    id: str
    name: str

class ILibraryItem(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    adult: bool
    age_rating: str
    age_rating_bucket: str
    artist: str
    author: str
    condition: str
    cover_images: List[ICoverImage]
    description: str
    display_name: str
    edition_id: str
    exclude_free_shipping: bool
    format: str
    genres: List[str]
    image_not_final: bool
    internal_id: int
    is_backorderable: bool
    is_in_stock: bool
    is_on_sale: bool
    is_pre_order: bool
    is_purchasable: bool
    isbn: str
    last_stock_update: str
    member_price: float
    name: str
    non_member_price: float
    page_count: int
    pre_book_date: str
    price_lvl_3: float
    promos: List[IPromoSale]
    publisher: str
    publisher_backorder: bool
    record_added_date: str
    record_updated_date: str
    release_date: str
    reprint_date: str
    retail_price: float
    sales: List[IPromoSale]
    series: str
    series_id: str
    stock_status: str
    themes: List[str]
    url_component: str
    volume: str
    weight: float

class ILibrary(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    items: Dict[str, ILibraryItem]
    last_update: str
    total: int
