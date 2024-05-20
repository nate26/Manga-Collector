
from datetime import datetime
import json
import time

from bs4 import BeautifulSoup
import requests

from src.data import Data
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

logger = MangaLogger(HostEnum.LOCAL).register_logger(__name__)
data = Data(HostEnum.LOCAL)

volumes_temp = data.get_volumes_data()
series_temp = data.get_series_data()
shop_temp = data.get_shop_data()

completed = 0

for isbn in shop_temp:
    logger.info('Fixing %s:', isbn)
    cr_shop = [shop for shop in shop_temp[isbn]['shops'] if shop['store'] == 'Crunchyroll'][0]
    other_shops = [shop for shop in shop_temp[isbn]['shops'] if shop['store'] != 'Crunchyroll']
    logger.info('Existing Shop Data: %s', json.dumps(shop_temp[isbn]['shops']))
    logger.info('Crunchyroll Shop Data: %s', json.dumps(cr_shop))
    logger.info('Other Shops Data: %s', json.dumps(other_shops))
    shop_temp[isbn]['shops'] = [
        cr_shop,
        *other_shops
    ]
    logger.info('New Shops Data: %s', json.dumps(shop_temp[isbn]['shops']))

    completed += 1
    progress = round((completed / len(series_temp)) * 50)
    remaining = 50 - progress
    percentage = round((completed / len(series_temp)) * 100, ndigits=2)
    print('progress: |' + ''.join(['=' for _ in range(progress)]) + ''.join(['-' for _ in range(remaining)]) + '| ' + str(percentage) + '%', end='\r')



print('Saving all files...')
data.save_all_files(volumes_temp, series_temp, shop_temp)
