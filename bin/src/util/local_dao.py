"""
Local DAO to get and write to local json files.
"""
import json
import traceback

from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

class LocalDAO:
    """
    A class used to get and write to local json files.

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
    get_json_file(path=str)
        Gets the data from a json file
    update_json_file(path=str, data=Any)
        Writes data to a json file
    """

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)
        self.host = host

    def open_file(self, file_path: str):
        '''
        Gets the data from a JSON file and copies it into a return object

        Parameters:
        - file_path (str): The file path to get the data from.

        Returns:
        - dict: The data from the given file path.

        Raises:
        - FileNotFoundError: The file path could not be found.
        - json.JSONDecodeError: The JSON data could not be decoded.
        - TypeError: The data type could not be determined.
        '''
        self.logger.info('Loading file %s...', file_path)
        try:
            with open(file_path, 'r', encoding='UTF-8') as outfile:
                outfile.flush()
                data = json.load(outfile)
                outfile.close()
                return data
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            self.logger.error(traceback.format_exc())
            self.logger.critical('Could not load file %s ... ending process', file_path)
            raise

    def save_file(self, file_path: str, data):
        '''
        Writes the given data to the given file path, and converts the data into a JSON format

        Parameters:
        - file_path (str): The file path to save the data to.
        - data: The data to save to the file path.

        Raises:
        - FileNotFoundError: The file path could not be found.
        - TypeError: The data type could not be determined.
        '''
        self.logger.info('Saving file %s...', file_path)
        try:
            with open(file_path, 'w', encoding='UTF-8') as outfile:
                outfile.flush()
                json.dump(data, outfile, indent=4, separators=(',', ': '))
                outfile.close()
        except (FileNotFoundError, TypeError):
            self.logger.error(traceback.format_exc())
            self.logger.critical('Could not save file %s ... ending process', file_path)
            raise

    def save_all_files(self, volumes_provided, series_provided, shop_provided):
        '''
        Saves all the given data structures to their respective files.

        Parameters:
        - volumes_provided: The volumes data structure to save to the file.
        - series_provided: The series data structure to save to the file.
        - shop_provided: The shop data structure to save to the file.
        '''
        self.logger.info('Saving all files...')

        # save volumes data
        try:
            self.save_file(FilePathEnum.VOLUMES.value[self.host.value], volumes_provided)
        except FileNotFoundError:
            self.logger.error(traceback.format_exc())
            self.logger.critical('Could not save volumes.json...')

        # save series data
        try:
            self.save_file(FilePathEnum.SERIES.value[self.host.value], series_provided)
        except FileNotFoundError:
            self.logger.error(traceback.format_exc())
            self.logger.critical('Could not save series.json...')

        # save shop data
        try:
            self.save_file(FilePathEnum.SHOP.value[self.host.value], shop_provided)
        except FileNotFoundError:
            self.logger.error(traceback.format_exc())
            self.logger.critical('Could not save shop.json...')

        self.logger.info('All files saved successfully')
