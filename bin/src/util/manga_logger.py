'''Class for setting up logging in for all modules.'''

import logging
import logging.config
from logging.handlers import RotatingFileHandler

from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.util.common_helper import CommonHelper

class MangaLogger:
    '''
    Class for setting up logging in for all modules.
    The logger must be registered using the `register_logger` method in each class.

    ...

    Parameters
    ----------
    host : HostEnum
        The the host machine to know where to access data for logging

    Attributes
    ----------
    common_helper : CommonHelper
        a utility class for common methods

    Methods
    -------
    register_logger(file_name: str)
        Registers the logger for the given file name.
    '''

    def __init__(self, host: HostEnum):
        '''
        Initializes the MangaLogger class.

        Parameters:
        - host (HostEnum): The host to set up logging for.
        '''
        self.common_helper = CommonHelper()
        file_name = self.common_helper.get_timezone_now('%Y-%m-%d_%H-%M-%S') + '.log'
        file_path = FilePathEnum.LOGS.value[host.value] + file_name
        logging.basicConfig(
            filename=file_path,
            format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            encoding='utf-8',
            level=logging.DEBUG
        )
        # my_handler = RotatingFileHandler(file_path, mode='a', maxBytes=5*1024*1024,
        #                                  backupCount=2, encoding='utf-8', delay=False)
        # my_handler.setFormatter(logging.Formatter(
        #     '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
        # ))
        # my_handler.setLevel(logging.DEBUG)
        # app_log = logging.getLogger('root')
        # app_log.setLevel(logging.DEBUG)
        # app_log.addHandler(my_handler)


    def register_logger(self, file_name: str):
        '''
        Registers the logger for the given file name.

        Parameters:
        - file_name (str): The name of the file to register the logger for.

        Returns:
        - logging.Logger: The logger for the given file name.
        '''
        return logging.getLogger(file_name)
