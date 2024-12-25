'''Module to scrape ISBN data from the CampusBooks website.'''

from datetime import datetime
import json
import re
import traceback
from xml.dom import NotFoundErr
from bs4 import BeautifulSoup
import requests

from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

class ScrapeISBN:
    '''
    A class used to scrape ISBN data from the CampusBooks website.

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
    get_isbn_details(soup_isbn_data=BeautifulSoup)
        Gets the details from the given ISBN soup object.
    get_shop_data(soup_isbn_data=BeautifulSoup, isbn_10=str)
        Gets all the valid shop details from the given isbn soup object.
    isbn_search(isbn=str)
        Searches for the given ISBN on the ISBN search website and returns the results.
    '''

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)

    def get_isbn_details(self, soup_isbn_data):
        '''
        Gets the details from the given ISBN soup object.

        Parameters:
        - soup_isbn_data: The soup object containing the ISBN data.

        Returns:
        - dict: The details from the given ISBN soup object.
        '''
        details = {
            'release_date': None,
            'publisher': None,
            'format': None,
            'pages': None,
            'authors': None,
            'isbn_10': None
        }
        try:
            text_tags = soup_isbn_data.find('div', {'class': 'book-info'}).find_all('dt')
            for tag in text_tags:
                if 'Released:' in tag.text and details['release_date'] is None:
                    release_date = tag.text.split(': ')[1]
                    try:
                        parsed_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', release_date.strip())
                        date = str(datetime.strptime(parsed_date, '%b %d, %Y').date())
                        today = datetime.now().strftime('%Y-%m-%d')
                        self.logger.info('Parsed release date: %s vs %s', date, today)
                        if date != today:
                            details['release_date'] = date
                        else:
                            self.logger.warning(
                                'Release date is today for future releases (incorrect): %s',
                                details['release_date']
                            )
                        self.logger.info('Found release date: %s', details['release_date'])
                    except (ValueError, AttributeError):
                        self.logger.error(traceback.format_exc())
                        self.logger.error('Release date is not in correct format... %s',
                                          release_date)
                if 'Publisher:' in tag.text and details['publisher'] is None:
                    details['publisher'] = tag.text.split(': ')[1].strip()
                    self.logger.info('Found publisher: %s', details['publisher'])
                if 'Format:' in tag.text and details['format'] is None:
                    format_details = tag.text.split(': ')[1]
                    if '  (' in format_details:
                        split_format = format_details.split('  (')
                        details['format'] = split_format[0].strip()
                        details['pages'] = int(split_format[1].split(' pages')[0].strip())
                        self.logger.info('Found pages: %s', details['pages'])
                    else:
                        details['format'] = format_details.strip()
                    self.logger.info('Found format: %s', details['format'])
                if 'Authors:' in tag.text and details['authors'] is None:
                    details['authors'] = tag.text.split(': ')[1].strip()
                    self.logger.info('Found authors: %s', details['authors'])
                if 'ISBN 10:' in tag.text and details['isbn_10'] is None:
                    details['isbn_10'] = tag.text.split(': ')[1].strip()
                    self.logger.info('Found ISBN 10: %s', details['isbn_10'])
                if None not in details.values():
                    break
            if None in details.values():
                self.logger.warning('Some ISBN detail attributes returned None: %s',
                                    json.dumps(details))
        except AttributeError as err:
            self.logger.error(traceback.format_exc())
            self.logger.warning(
                'Could not find all book details from isbn... ending process because %s',
                err
            )
            self.logger.warning('Details found: %s', json.dumps(details))
        except NotFoundErr as err:
            self.logger.warning(
                'Could not find all book details from isbn... ending process because %s',
                err
            )
            self.logger.warning('Details found: %s', json.dumps(details))
        return details

    def get_shop_data(self, soup_isbn_data, isbn_10: str, isbn: str):
        '''
        Gets all the valid shop details from the given isbn soup object.

        Parameters:
        - soup_isbn_data: The soup object containing the ISBN data.
        - isbn_10 (str): The ISBN-10 number to search for.

        Returns:
        - list: The list of shop details for the given ISBN.
        '''
        shops = []
        try:
            offers = soup_isbn_data.find('div', {'class': 'standard-offers'})
            if offers is None:
                return []

            stores = offers.find_all('tr')
            for store in stores:
                try:
                    if store.find('td', {'class': 'logo'}).find('span').attrs['title'].strip() \
                        != 'Amazon Mkt Used':
                        raise AttributeError('could not find "Amazon Mkt Used" in page')
                    self.logger.info('Found record for shop: Amazon')
                    condition = store.find('td', {'class': 'condition'}).attrs['data-condition']
                    shops.append({
                        'item_id': isbn + 'Amazon' + condition,
                        'isbn': isbn,
                        'store': 'Amazon',
                        'condition': condition,
                        'url': 'https://www.amazon.com/dp/' + isbn_10,
                        'price': float(store.find('td', {'class': 'total'})
                            .text.strip().replace('$', '')),
                        'stock_status': None,
                        'last_stock_update': None, #* gets set later
                        'coupon': '',
                        'is_on_sale': False,
                        'exclusive': False,
                        'promotion': '',
                        'promotion_percentage': None,
                        'backorder_details': None,
                        'dropped_check': False
                    })
                    self.logger.info('Shop details added: %s', shops[-1])
                except AttributeError:
                    # self.logger.warning('Could not find shop details for Amazon... skipping')
                    # self.logger.error(traceback.format_exc())
                    continue
        except AttributeError as err:
            self.logger.warning(
                'Could not find shop details from isbn... ending process because %s',
                err
            )
            self.logger.error(traceback.format_exc())
        return shops

    def isbn_search(self, isbn: str):
        '''
        Searches for the given ISBN on the ISBN search website and returns the results.

        Parameters:
        - isbn (str): The ISBN to search for.

        Returns:
        - dict: The results of the ISBN search.
        '''
        soup_isbn_data = BeautifulSoup(
            requests.get('https://www.campusbooks.com/search/' + isbn + '?buysellrent=buy',
                         timeout=30)
                .text,
            'html.parser'
        )
        isbn_details = self.get_isbn_details(soup_isbn_data)
        return {
            'details': isbn_details,
            'shops': self.get_shop_data(soup_isbn_data, isbn_details['isbn_10'], isbn)
        }
