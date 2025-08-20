import math
import time
import traceback
from datetime import datetime, timedelta
import requests
from enums.file_path_enum import FilePathEnum
from enums.host_enum import HostEnum
from interfaces.iright_stuf_item import IRightStufItem
from src.manga.manga_enricher import MangaEnricher
from src.series.series_enricher import SeriesEnricher
from util.common_helper import CommonHelper
from util.manga_logger import MangaLogger
from util.local_dao import LocalDAO

class MangaScraper:
    
    def __init__(self, host: HostEnum):
        self.common_helper = CommonHelper()
        self.manga_enricher = MangaEnricher(host)
        self.series_enricher = SeriesEnricher(host)
        self.local_dao = LocalDAO(host)
        self.logger = MangaLogger(host, __name__)
        self.host = host.value
        self.formats = ['Manga', 'Manhua', 'Manhwa', 'Novels']
        if self.host == HostEnum.MOCK.value:
            self.publishers = ['MOCK']
        else:
            self.publishers = ['ABLAZE', 'ACONYTE', 'AIRSHIP', 'ALGONQUIN YOUNG READERS', 'ATRIA BOOKS', 'CENTRAL PARK MEDIA',
                               'CROSS INFINITE WORLD', 'DARK HORSE', 'DARK HORSE MANGA', 'DC COMICS', 'DEL REY', 
                               'DELACORTE BOOKS FOR YOUNG READERS', 'DENPA', 'DIGITAL MANGA PUBLISHING', 'DRAMAQUEEN',
                               'DRAWN--AND--QUARTERLY', 'EIGOMANGA', 'FANFARE', 'FANTAGRAPHICS', 'FIRST SECOND', 'GEN MANGA', 
                               'GHOST SHIP', 'GLACIER BAY BOOKS', 'IZE PRESS', 'JADED SKETCH ILLUSTRATION', 'J-NOVEL CLUB', 
                               'J-NOVEL HEART', 'KAITEN BOOKS', 'KNOPF PUBLISHERS', 'KODANSHA', 'KODANSHA COMICS', 'KUMA', 
                               'LAST GASP', 'MAD NORWEGIAN PRESS', 'MEDIA BLASTERS', 'NBM PUBLISHING', 'NET COMICS', 'ONE PEACE', 
                               'PANTHEON', 'PENGUIN WORKSHOP', 'PIED PIPER', 'POPOTAME BOOK GALLERY', 'QUIRK BOOKS', 'SEVEN SEAS',
                               'SEVEN SEAS BL', 'SEVEN SEAS GL', 'SHAMBHALA', 'SHOJO BEAT', 'SQUARE ENIX BOOKS', 'SQUARE ENIX MANGA',
                               'STAR FRUIT BOOKS', 'STEAMSHIP', 'STONE BRIDGE PRESS', 'SUBLIME', 'TENTAI BOOKS', 'TITAN BOOKS',
                               'TITAN COMICS', 'TITAN MANGA', 'TOKYO SHOCK', 'TOKYOPOP', 'TUTTLE', 'UDON ENTERTAINMENT', 
                               'VAST VISUAL', 'VERTICAL', 'VIZ BOOKS', 'WEBTOON UNSCROLLED', 'YAOI PRESS', 'YEN ON', 'YEN PRESS']
        self.elapsed_network_time = 0
        self.elapsed_processing_time = 0
        

    def get_items(self, page: int, form: str, publisher: str):
        time.sleep(3)
        start = datetime.now()
        offset = page * 100
        try:
            if self.host == HostEnum.MOCK.value:
                return self.local_dao.get_json_file('./db/mocks/mock-rs-response.json')
            else:
                url = 'https://www.rightstufanime.com/api/items?' + \
                    'c=' + '546372' + \
                    '&country=' + 'US' + \
                    '&currency=' + 'USD' + \
                    '&custitem_damaged_type=' + 'New' + \
                    '&custitem_rs_web_class=' + form + \
                    '&custitem_rs_publisher=' + publisher + \
                    '&fieldset=' + 'details' + \
                    '&language=' + 'en' + \
                    '&limit=' + str(100) + \
                    '&n=' + str(2) + \
                    '&offset=' + str(offset) + \
                    '&pricelevel=' + str(2) + \
                    '&sort=' + 'custitem_rs_release_date%3Adesc' + \
                    '&use_pcv=' + 'F'
                response = requests.get(url).json()
                self.elapsed_network_time += (datetime.now() - start).total_seconds()
                return response
        except:
            self.logger.warning('Page: ' + str(page) + ', Format: ' + form + ', Publisher: ' + publisher)
            self.logger.error('Failed to get data from RightStuf', traceback.format_exc())

    def get_all_items(self):
        # configure values:
        #   custitem_rs_publisher
        #   custitem_rs_sale
        #   custitem_rs_specials_and_promos
        #   custitem_rs_specialty_product
        #   custitem_rs_genre
        #   custitem_rs_themes
        #   custitem_rs_age_rating
        #   custitem_damaged_type
        try:
            self.local_dao.update_json_file(FilePathEnum.EDITING.value[self.host], {'editing': True})
            all_items = self.local_dao.get_json_file(FilePathEnum.ALL_ITEMS.value[self.host]).get('items')
            series = self.local_dao.get_json_file(FilePathEnum.SERIES.value[self.host])
            
            for publisher in self.publishers:
                page = 0
                pages = 1
                first = True
                while page < pages:
                    response = self.get_items(page, 'Manga%2CManhua%2CManhwa%2CNovels', publisher)
                    for item in response.get('items'):
                        start = datetime.now()
                        try:
                            (isbn, enriched_volume) = self.manga_enricher.unpack_item(
                                IRightStufItem(item),
                                all_items
                            )
                            (series_id, enriched_series, edition_id) = self.series_enricher.update_series(
                                enriched_volume,
                                series
                            )
                            enriched_volume.series_id = series_id
                            enriched_volume.edition_id = edition_id
                            all_items[isbn] = vars(enriched_volume)
                            series[series_id] = enriched_series
                        except:
                            self.logger.warning('Volume Object: ')
                            self.logger.warning(item)
                            self.logger.error('Failed to enrich volume: ' + item['itemid'], traceback.format_exc())
                            self.logger.warning('Continuing to process records...')
                        self.elapsed_processing_time += (datetime.now() - start).total_seconds()
                    if first:
                        pages = math.ceil(response.get('total') / 100)
                    first = False
                    page += 1

                    self.local_dao.update_json_file(FilePathEnum.ALL_ITEMS.value[self.host], {
                        'total': len(all_items),
                        'items': all_items,
                        'last_update': self.common_helper.get_timezone_now()
                    })
                    self.local_dao.update_json_file(FilePathEnum.SERIES.value[self.host], series)

            self.local_dao.update_json_file(FilePathEnum.EDITING.value[self.host], {'editing': False})
        except:
            self.local_dao.update_json_file(FilePathEnum.EDITING.value[self.host], {'editing': False})
            self.logger.error('Failed to scrape data', traceback.format_exc())

    def run(self):
        start = datetime.now()
        self.logger.info('Start Time (ET): ' + self.common_helper.get_timezone_now())
        self.get_all_items()
        self.logger.info('End Time (ET): ' + self.common_helper.get_timezone_now())
        self.logger.info('Total Network Time: ' + str(timedelta(seconds=self.elapsed_network_time)))
        self.logger.info('Total Processing Time: ' + str(timedelta(seconds=self.elapsed_processing_time)))
        self.logger.info('Total Elapsed Time: ' + str(timedelta(seconds=(datetime.now() - start).total_seconds())))
