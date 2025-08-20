'''Interface for Volume'''

from typing import List

class ICoverImage(dict):
    '''Cover image details of a book'''
    __getattr__ = dict.get
    name: str
    url: str

class IVolume(dict):
    '''Volume details for a book'''
    __getattr__ = dict.get
    isbn: str
    brand: str
    series: str
    series_id: str
    display_name: str
    name: str
    category: str
    volume: str
    url: str
    record_added_date: str
    record_updated_date: str
    release_date: str
    publisher: str
    format: str
    pages: int
    authors: str
    isbn_10: str
    cover_images: List[ICoverImage]
    description: str
