"""
Local DAO to get and write to local json files.
"""
import json
import traceback

from enums.host_enum import HostEnum
from util.manga_logger import MangaLogger

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
        self.logger = MangaLogger(host, __name__)

    def get_json_file(self, path: str):
        """Gets the data from a json file and copies it into a return object

        Parameters
        ----------
        path : str
            The file path for the json file you want to load

        Raises
        ------
        FileNotFoundError
            If the given file does not exist or could not be found.
        JSONDecodeError:
            If the file's contents are not in a valid JSON format.
        TypeError:
            If the file's contents not in str, bytes, or bytesarray format.
        """
        try:
            with open(path, 'r', encoding='UTF-8') as outfile:
                outfile.flush()
                data = json.load(outfile)
                outfile.close()
                return data
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            self.logger.error('Could not load file ' + path + ' ... ending process', traceback.format_exc())
            raise
    
    def update_json_file(self, path: str, data):
        """Writes the given data to the given file path, and converts the
        data into a json format.

        Parameters
        ----------
        path : str
            The file path for the json file you want to save to
        data : Any
            A valid json data format to save to the given file path

        Raises
        ------
        FileNotFoundError
            If the given file does not exist or could not be found.
        TypeError:
            If the encoder is unable to serialize the object.
        """
        try:
            with open(path, 'w', encoding='UTF-8') as outfile:
                outfile.flush()
                outfile.write(json.dumps(data))
                outfile.close()
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            self.logger.error('Could not save data to ' + path + ' ... ending process', traceback.format_exc())
            raise
