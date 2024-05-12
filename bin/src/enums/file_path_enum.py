'''Enum for file paths for different hosts.'''
from enum import Enum

class FilePathEnum(Enum):
    '''Enum for file paths for different hosts.'''

    VOLUMES = {
        'local': './db/volumes.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/volumes.json',
        'mock': './db/volumes.json'
    }
    SERIES = {
        'local': './db/series.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/series.json',
        'mock': './db/series.json'
    }
    SHOP = {
        'local': './db/shop.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/shop.json',
        'mock': './db/shop.json'
    }
    EDITING = {
        'local': './db/editing.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/editing.json',
        'mock': './db/mocks/mock-editing.json'
    }
    LOGS = {
        'local': './logs/',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/logs/',
        'mock': './logs/'
    }
