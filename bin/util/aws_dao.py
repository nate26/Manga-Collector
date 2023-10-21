"""
Local DAO to get and write to AWS Dynamo DB.
"""
import json
import traceback
from datetime import datetime, timedelta

import requests

from enums.host_enum import HostEnum
from util.manga_logger import MangaLogger

class AWSDAO:
    """
    A class used to get and write to AWS Dynamo DB.

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
    get_data(url=str)
        Gets the data from the AWS directory
    post_data(url=str, data=Any)
        Writes data to AWS directory
    """

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host, __name__)

    def get_data(self, url: str):
        """Gets data from an AWS directory and returns the contents as a json

        Parameters
        ----------
        url : str
            The AWS url to get the data from

        Raises
        ------
        JSONDecodeError:
            If the response contents from AWS are not in a valid JSON format.
        """
        try:
            start = datetime.now()
            response = requests.get(url).json()
            end = (datetime.now() - start).total_seconds()
            self.logger.info('Time to get data from AWS: ' + str(timedelta(seconds=end)))
            return response
        except:
            self.logger.error('Could not get data from ' + url + ' ... ending process', traceback.format_exc())
            raise

    def post_data(self, url: str, contents) -> str:
        """Writes data to an AWS directory and returns a string response from the service

        Parameters
        ----------
        url : str
            The AWS url to post the data to

        Raises
        ------
        """
        try:
            start = datetime.now()
            response = requests.post(url, contents).json()
            end = (datetime.now() - start).total_seconds()
            self.logger.info('Time to post data to AWS: ' + str(timedelta(seconds=end)))
            return response
        except:
            self.logger.error('Could not post data to ' + url + ' ... ending process', traceback.format_exc())
            raise
