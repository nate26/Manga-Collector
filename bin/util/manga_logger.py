import logging
import logging.config
import os

from enums.file_path_enum import FilePathEnum
from enums.host_enum import HostEnum
from util.common_helper import CommonHelper

class MangaLogger:

    def __init__(self, host: HostEnum, file_name: str):
        self.common_helper = CommonHelper()
        file_name = self.common_helper.get_timezone_now('%Y-%m-%d') + ' output' + '.log'
        file_path = FilePathEnum.LOGS.value[host.value] + file_name
        if file_name not in os.listdir(os.getcwd() + '\\logs'):
            self.__create_file(file_path)
        logging.basicConfig(
            filename=file_path,
            encoding='utf-8',
            level=logging.INFO,
            format='%(asctime)s|%(name)s|%(levelname)s - %(message)s')
        
    def __create_file(self, path):
        with open(path, 'w+', encoding='UTF-8') as outfile:
            outfile.close()

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg, traceback):
        logging.error(traceback)
        logging.error(msg)