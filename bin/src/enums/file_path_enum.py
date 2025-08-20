'''Enum for file paths for different hosts.'''
from enum import Enum

class FilePathEnum(Enum):
    '''Enum for file paths for different hosts.'''

    MANGA_SERVER = {
        'local': 'http://localhost:4000/api',
        'server': 'http://localhost:4000/api',
        'mock': 'http://localhost:4000/api'
    }
    VOLUMES = {
        'local': './db/volumes.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/volumes.json',
        'mock': './db/mocks/volumes.json'
    }
    SERIES = {
        'local': './db/series.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/series.json',
        'mock': './db/mocks/series.json'
    }
    SHOP = {
        'local': './db/shop.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/shop.json',
        'mock': './db/mocks/shop.json'
    }
    USERS = {
        'local': './db/users.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/users.json',
        'mock': './db/mocks/users.json'
    }
    VAULT = {
        'local': './db/vault.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/vault.json',
        'mock': './db/mocks/vault.json'
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
