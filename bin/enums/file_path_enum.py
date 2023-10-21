from enum import Enum

class FilePathEnum(Enum):
    ALL_ITEMS = {
        'local': './db/items.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/items.json',
        'mock': './db/items.json'
        # 'mock': './db/mocks/mock-items.json'
    }
    SERIES = {
        'local': './db/series.json',
        'server': 'MangaTracker/Manga-Tracker-UI/bin/db/series.json',
        'mock': './db/series.json'
        # 'mock': './db/mocks/mock-series.json'
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
