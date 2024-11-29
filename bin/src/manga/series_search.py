'''Module to search for series information from the MangaUpdates API.'''

import difflib
import json
import traceback
import requests
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

class SeriesSearch:
    '''
    Class to search for series information from the MangaUpdates API.

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
    get_top_themes(series_resp=dict)
        Parsing the top themes from the MangaUpdates API response.
    get_status(series_resp=dict)
        Parsing the status from the MangaUpdates API response.
    get_series_by_id(series_id=str)
        Gets the series information from the given series ID.
    calculate_confidence(series_name=str, title=str)
        Calculates the confidence level for the given series name and title.
    search_series(series_name=str, category=str, volume_name=str)
        Gets the series ID from the given series name and format.
    '''

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)
        self.series_cache = {}

    def get_top_themes(self, series_resp):
        '''
        Parsing the top themes from the MangaUpdates API response.

        Parameters:
        - series_resp (dict): The response from the MangaUpdates API.

        Returns:
        - list: The top themes from the given response.
        '''
        self.logger.info('Getting top themes...')
        return sorted(
            [
                {
                    'theme': category['category'],
                    'votes': category['votes_plus'] - category['votes_minus']
                }
                for category in series_resp['categories']
                if (category['votes_plus'] - category['votes_minus']) > 0
            ],
            key = lambda x: x['votes'],
            reverse=True
        )[:15]

    def get_status(self, series_resp):
        '''
        Parsing the status from the MangaUpdates API response.

        Parameters:
        - series_resp (dict): The response from the MangaUpdates API.

        Returns:
        - str: The status from the given response.
        '''
        self.logger.info('Getting status...')
        if series_resp['status'] is not None:
            if 'Ongoing' in series_resp['status']:
                return 'Ongoing'
            elif 'Complete' in series_resp['status']:
                return 'Completed'
            elif 'Hiatus' in series_resp['status']:
                return 'Hiatus'
            elif 'Cancelled' in series_resp['status'] or 'Discontinued' in series_resp['status']:
                return 'Cancelled'
        else:
            return 'Unknown'

    def get_series_by_id(self, series_id: str):
        '''
        Gets the series information from the given series ID.

        Parameters:
        - series_id (str): The ID of the series to search for.

        Returns:
        - dict: The series information from the given series ID.

        Raises:
        - requests.exceptions.RequestException: An error occurred while getting the series details.
        '''
        self.logger.info('Getting series details for %s...', series_id)
        try:
            if series_id in self.series_cache:
                parsed_series_data = self.series_cache[series_id]
                self.logger.info('Pulled series from local cache: %s',
                                 json.dumps(parsed_series_data))
            else:
                series_resp = requests.get('https://api.mangaupdates.com/v1/series/' + series_id,
                                        timeout=30).json()
                self.logger.info('Series recieved from api: %s', json.dumps(series_resp))
                parsed_series_data = {
                    'series_id': str(series_resp['series_id']),
                    'title': series_resp['title'],
                    'associated_titles': [title['title'] for title in series_resp['associated']],
                    'editions': [],
                    'url': series_resp['url'],
                    'category': series_resp['type'],
                    'description': series_resp['description'],
                    'cover_image': series_resp['image']['url']['original'],
                    'genres': [genre['genre'] for genre in series_resp['genres']],
                    'themes': self.get_top_themes(series_resp),
                    'latest_chapter': series_resp['latest_chapter'],
                    'release_status': series_resp['status'],
                    'status': self.get_status(series_resp),
                    'authors': [
                        { 'name': author['name'], 'type': author['type'] }
                        for author in series_resp['authors']
                    ],
                    'publishers': [
                        { 'name': publisher['publisher_name'], 'type': publisher['type'] }
                        for publisher in series_resp['publishers']
                    ],
                    'bayesian_rating': series_resp['bayesian_rating'],
                    'rank': series_resp['rank']['position']['year'],
                    'recommendations': [str(rec['series_id']) for rec in series_resp['recommendations']]
                }
            return parsed_series_data
        except requests.exceptions.RequestException:
            self.logger.error('Could not get series details for %s... ending process', series_id)
            self.logger.error(traceback.format_exc())
            raise

    def calculate_confidence(self, series_name: str, title: str):
        '''
        Calculates the confidence level for the given series name and title.

        Parameters:
        - series_name (str): The name of the series to search for.
        - title (str): The title to search for.

        Returns:
        - float: The confidence level for the given series name and title.
        '''
        return difflib.SequenceMatcher(None, series_name.lower(), title.lower()).ratio()

    def save_series_cache(self, series_id: str, series_data: dict):
        '''
        Saves the series data to the cache.

        Parameters:
        - series_id (str): The ID of the series to save.
        - series_data (dict): The data of the series to save.
        '''
        self.series_cache[series_id] = series_data
        self.logger.info('Added series to local cache: %s', json.dumps(series_data))

    def search_series(self, series_name: str, category: str, volume_name: str):
        '''
        Gets the series ID from the given series name and format.

        Parameters:
        - series_name (str): The name of the series to search for.
        - category (str): The category of the series to search for.
        - volume_name (str): The name of the volume to search for.

        Returns:
        - dict: The series information from the given series name and format.
        '''
        category_conversion = {
            '': None,
            'light-novels': 'novel',
            'manhwa': 'manhwa',
            'manhua': 'manhua',
            'novels': 'novel',
            'manga': 'manga',
            'manga-bundles': 'manga'
        }
        series_category = category_conversion[category]
        self.logger.info('Searching for series ID for ["%s", "%s" ]...',
                         series_name, series_category)
        search_data = {
            'search': series_name,
            'stype': 'title'
        }
        try:
            if series_name is None:
                raise AttributeError('series name is None')

            series_resp = requests.post('https://api.mangaupdates.com/v1/series/search',
                                        search_data, timeout=30).json()
            # only used if no exact match is found
            closest_series_match = None
            for series in [series_resp['results'][0]]:
                series_details = self.get_series_by_id(str(series['record']['series_id']))
                self.logger.info('Checking series: %s', json.dumps(series_details))

                # series category must match
                if series_details['category'].lower() == series_category.lower():
                    all_titles = [
                        title for title
                        in [ series_details['title'], *series_details['associated_titles'] ]
                    ]

                    # check for exact equality in title or associated titles
                    for title in all_titles:
                        if title.lower() == series_name.lower():
                            series_details['series_match_confidence'] = 1
                            series_details['title'] = title # update title to closest match
                            self.logger.info('Exact series match found: %s',
                                             series_details['title'])
                            self.save_series_cache(series['record']['series_id'], series_details)
                            return series_details

                    # set first found to match category to a low confidence match
                    series_details['series_match_confidence'] = 0.1
                    closest_series_match = series_details

                    # check for partial equality in title or associated titles
                    for title in all_titles:
                        confidence = max(
                            # if series title or associated title is in volume name
                            # case: 'Re:ZERO Ex' in 'Re:Zero Ex Novel Volume 1' = True
                            self.calculate_confidence(series_name, title),
                            # if series name is in title or associated title, or vice versa
                            # case: 'Re:Zero' in 'Re:ZERO Ex (Novel)' = True
                            self.calculate_confidence(volume_name, title)
                        )
                        if series_details['series_match_confidence'] < confidence:
                            series_details['series_match_confidence'] = confidence
                            closest_series_match = series_details
                            self.logger.info(
                                'Partial series match for [%s, %s] found with confidence %s: %s',
                                series_name,
                                volume_name,
                                str(series_details['series_match_confidence']),
                                title
                            )
                            series_details['title'] = title # update title to closest match

            if closest_series_match is not None:
                self.logger.info('Closest series match with confidence %s: %s',
                            closest_series_match['series_match_confidence'],
                            json.dumps(closest_series_match))
                self.save_series_cache(series['record']['series_id'], series_details)
                return closest_series_match
        except (requests.exceptions.RequestException, IndexError, AttributeError):
            self.logger.error('Could not get series ID for "%s"... ending process', series_name)
            self.logger.error(traceback.format_exc())

        self.logger.warning('Could not find any matching series ID for "%s"... ending process',
                            series_name)
        return {
            'series_id': None,
            'title': None,
            'associated_titles': [],
            'editions': [],
            'url': None,
            'category': None,
            'description': None,
            'cover_image': None,
            'genres': [],
            'themes': [],
            'latest_chapter': None,
            'release_status': None,
            'status': None,
            'authors': [],
            'publishers': [],
            'bayesian_rating': None,
            'rank': None,
            'recommendations': [],
        }
