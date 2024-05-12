from typing import List

from interfaces.ilibrary import ILibraryItem


class ISeriesVolume(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    isbn: str
    volume: str
    release_date: str

class IEdition(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    edition: str
    edition_id: str
    format: str
    volumes: List[ISeriesVolume]

class ISeries(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    title: str
    series_id: str
    editions: dict[str:IEdition]

    

class IEditionEnriched(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    edition: str
    edition_id: str
    format: str
    volumes: List[ILibraryItem]