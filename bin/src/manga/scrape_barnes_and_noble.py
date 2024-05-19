'''Module to scrape shop data from Barnes and Noble.'''

from datetime import datetime
import traceback

from bs4 import BeautifulSoup
import requests

from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

class ScrapeBarnesAndNoble:
    '''
    A class used to scrape shop data from Barnes and Noble.

    ...

    Parameters
    ----------
    host : HostEnum
        The the host machine to know where to access data for logging

    Attributes
    ----------
    logger : MangaLogger
        a logging utility for info, warning, and error logs

    Methods
    -------
    get_barnes_and_noble_data(isbn=str, vol_shop_data=list)
        Gets the Barnes & Noble data for the given ISBN.
    '''

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)

    def get_barnes_and_noble_data(self, isbn: str, vol_shop_data: list):
        '''
        Gets the Barnes & Noble data for the given ISBN.

        Parameters:
        - isbn (str): The ISBN to search for.
        - vol_shop_data (list): The list of shop data for the given volume.

        Returns:
        - dict: The Barnes & Noble data for the given ISBN, or None if the data could not
        be retrieved.
        '''
        try:
            url = 'https://barnesandnoble.com/w/?ean=' + isbn
            self.logger.info('Getting Barnes & Noble data for %s...', isbn)
            soup_bn_data = BeautifulSoup(
                requests.get(url, timeout=30).text,
                'html.parser'
            )
            formats = soup_bn_data.find_all('div', {'class': 'pdp-commerce-format'})
            valid_format = [format for format in formats if 'Paperback' in format.text]
            store_price = float(valid_format[0].find('div', {'class': 'format-price'})
                                .text.strip().replace('$', '')) \
                                    if len(valid_format) > 0 else None
            stock_status = soup_bn_data.find('div', {'class': 'purchase-add-to-cart'}) \
                .find('div', {'class': 'add-to-cart-button'}).attrs['value']
            existing_bn_data = list(filter(lambda x: x['store'] == 'Barnes & Noble',
                                           vol_shop_data))
            is_new_entry = len(existing_bn_data) == 0
            existing_stock_status = existing_bn_data[0]['stock_status'] \
                if not is_new_entry else None
            return {
                'store': 'Barnes & Noble',
                'condition': 'New',
                'url': url,
                'store_price': store_price,
                'stock_status': stock_status,
                'last_stock_update': str(datetime.now()) \
                    if is_new_entry and stock_status == existing_stock_status \
                        else existing_bn_data[0]['last_stock_update'],
                'coupon': '',
                'is_on_sale': False
            }
        except (requests.exceptions.RequestException, AttributeError):
            self.logger.critical('Could not get Barnes & Noble data for %s ... ending process',
                                 isbn)
            self.logger.error(traceback.format_exc())
            return None
