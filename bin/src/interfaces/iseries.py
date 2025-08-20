'''Interfaces for Series details'''

from typing import List

class ISeriesVolume(dict):
    '''Volume details for a series'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    isbn: str
    volume: str
    category: str

class ISeriesThemes(dict):
    '''Themes details for a series'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    theme: str
    votes: int

class ISeriesDetails(dict):
    '''Details for a series object'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    name: str
    type: str

class ISeries(dict):
    '''Series details for a book'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    series_id: str
    title: str
    associated_titles: List[str]
    url: str
    category: str
    series_match_confidence: float
    volumes: List[ISeriesVolume]
    description: str
    cover_image: str
    genres: List[str]
    themes: List[ISeriesThemes]
    latest_chapter: int
    release_status: str
    status: str
    authors: List[ISeriesDetails]
    publishers: List[ISeriesDetails]
    bayesian_rating: float
    rank: int
    recommendations: List[int]
