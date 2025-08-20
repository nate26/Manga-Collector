'''Interface for volume display data for a book'''

from typing import List
from src.interfaces.icollection import ICollection
from src.interfaces.iseries import ISeries
from src.interfaces.ishop import IStoreItem
from src.interfaces.ivolume import IVolume
from src.interfaces.iwishlist import IWishlist

class IPartialSeries(dict):
    '''Partial series data for a book'''
    series_id: str
    url: str

class IPartialStoreItem(dict):
    '''Partial store item data for a book'''
    store: str
    url: str

class IVolumeDisplay(IVolume, dict):
    '''Volume display data for a book'''
    primary_cover_image_url: str
    other_images: List[str]
    series_data: ISeries | IPartialSeries
    retail_price: float
    purchase_options: IStoreItem | IPartialStoreItem
    user_collection_data: List[ICollection]
    user_wishlist_data: List[IWishlist]
