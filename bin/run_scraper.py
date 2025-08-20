from src.util.manga_logger import MangaLogger
from src.manga.scrape_crunchyroll import ScrapeCrunchyroll
from src.enums.host_enum import HostEnum

manga_enricher = ScrapeCrunchyroll(HostEnum.LOCAL)
manga_enricher.run_scraper()

logger = MangaLogger(HostEnum.LOCAL).register_logger(__name__)
logger.info('-----------------------------------------------------------------------------')
logger.info('---------------------------------PROCESS END---------------------------------')
logger.info('-----------------------------------------------------------------------------')
