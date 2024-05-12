from typing import List
from enums.format_enum import FormatEnum
from interfaces.icover_image import CoverImage
from interfaces.isale import ISale


class IVolume(object):
    
    def __init__(self, obj={}):
        for key in obj:
            setattr(self, key, obj[key])

    record_added_date: str = None
    last_stock_update: str = None
    record_updated_date: str = None
    isbn: str = None
    series_id: str = None
    edition_id: str = None

    # volume details
    display_name: str = None
    series: str = None
    name: str = None
    format: FormatEnum = None
    volume: str = None
    artist: str = None
    author: str = None
    cover_images: List[CoverImage] = None
    description: str = None
    genres: List[str] = None
    themes: List[str] = None
    publisher: str = None
    age_rating: str = None
    age_rating_bucket: str = None
    page_count: int = None
    adult: bool = None
    weight: float = None
    internal_id: int = None
    url_component: str = None

    # item status
    is_in_stock: bool = None
    is_purchasable: bool = None
    is_backorderable: bool = None
    is_pre_order: bool = None
    stock_status: str = None
    is_on_sale: bool = None
    promos: List[ISale] = None
    sales: List[ISale] = None
    publisher_backorder: bool = None
    image_not_final: bool = None
    condition: str = None
    exclude_free_shipping: bool = None

    # prices
    retail_price: float = None
    non_member_price: float = None
    member_price: float = None
    price_lvl_3: float = None

    # dates
    release_date: str = None
    reprint_date: str = None
    pre_book_date: str = None

    contained_isbns: List[str] = None
