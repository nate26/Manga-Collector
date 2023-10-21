from enums.host_enum import HostEnum
from src.manga.manga_scraper import MangaScraper
from util.manga_logger import MangaLogger


manga_enricher = MangaScraper(HostEnum.MOCK)
manga_enricher.run()

logger = MangaLogger(HostEnum.MOCK, __name__)
logger.info('-----------------------------------------------------------------------------')
logger.info('---------------------------------PROCESS END---------------------------------')
logger.info('-----------------------------------------------------------------------------')
