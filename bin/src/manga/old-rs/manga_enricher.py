import re
import json
from collections.abc import MutableMapping
import traceback
from typing import List, Tuple
from enums.file_path_enum import FilePathEnum
from enums.format_enum import FormatEnum
from interfaces.iseries import ISeries
from util.local_dao import LocalDAO
from interfaces.iright_stuf_item import IRightStufItem
from interfaces.isale import ISale
from interfaces.ivolume import IVolume

from util.common_helper import CommonHelper
from util.manga_logger import MangaLogger

class MangaEnricher:

    def __init__(self, host):
        self.common_helper = CommonHelper()
        self.logger = MangaLogger(host, __name__)
        self.local_dao = LocalDAO(host)
        self.host = host.value

    def flatten_dict(self, mut_mapping: MutableMapping, parent_key: str='', sep: str='.') -> MutableMapping:
        items = []
        for k, v in mut_mapping.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def get_cover_images(self, item_id: str, itemimages_detail: dict, display_name: str):
        try:
            if len(itemimages_detail.keys()) == 0:
                return None
            flat = self.flatten_dict(itemimages_detail)
            urls = []
            for url in flat.keys():
                if url[-5:] == '.urls':
                    for obj in flat.get(url):
                        urls.append({ 'name': obj.get('altimagetext'), 'url': obj.get('url') })
                elif url[-4:] == '.url':
                    urls.append({ 'name': url.split('.')[-2], 'url': flat.get(url) })
            if len(urls) == 0:
                self.logger.warning('no image for ' + item_id)
            return urls
        except:
            self.logger.warning('Image Obj:')
            self.logger.warning(itemimages_detail)
            self.logger.error('cover image error for ' + display_name, traceback.format_exc())
            return None

    def parse_name(self, display_name: str, form: str):
        name_split = []
        is_box_set = False
        if re.search(' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name):
            name_split = re.split(
                ' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name)
        elif re.search(' [()]?Vol[a-z]?[()]? \d+\.?\d*', display_name):
            name_split = re.split(
                ' [()]?Vol[a-z]?[()]? \d+\.?\-?\d*', display_name)
        elif re.search(' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name):
            name_split = re.split(
                ' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name)
        elif re.search(' [()]?Box Set[()]? \d+\.?\-?\d*', display_name):
            name_split = re.split(' [()]?Box Set[()]? \d+\.?\-?\d*', display_name)
            name_split[0] += ' Box Set'
            is_box_set = True
        else:
            name_split = re.split(
                ' [()]?' + form + '[a-z]?[()]? \d+\.?\-?\d*', display_name)
        name = ''.join(name_split)
        if not is_box_set:
            name = name.replace(' ' + form, '')
        return name

    def parse_volume(self, display_name: str, form: str):
        if re.search(' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name):
            return re.search('\d+\.?\-?\d*', re.search(' [()]?Volume[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)).group(0)
        if re.search(' [()]?Vol[a-z]?[()]? \d+\.?\d*', display_name):
            return re.search('\d+\.?\-?\d*', re.search(' [()]?Vol[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)).group(0)
        if re.search(' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name):
            return re.search('\d+\.?\-?\d*', re.search(' [()]?Graphic Novel[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)).group(0)
        if re.search(' [()]?Box Set[()]? \d+\.?\-?\d*', display_name):
            return re.search('\d+\.?\-?\d*', re.search(' [()]?Box Set[()]? \d+\.?\-?\d*', display_name).group(0)).group(0)
        if re.search(' [()]?' + form + '[a-z]?[()]? \d+\.?\-?\d*', display_name):
            return re.search('\d+\.?\-?\d*', re.search(' [()]?' + form + '[a-z]?[()]? \d+\.?\-?\d*', display_name).group(0)).group(0)
        return None

    def is_on_sale(self, sales: List[str]):
        j_sales = json.loads(sales)
        promos = j_sales.get('specialsAndPromosIds')
        return '1' in promos or \
            '2' in promos or \
            '12' in promos or \
            '14' in promos or \
            '21' in promos or \
            '31' in promos or \
            '35' in promos or \
            '43' in promos or \
            len(j_sales.get('sales')[0]) > 0

    def get_promos(self, promos: List[str]) -> List[ISale]:
        all_promos = []
        for promo in list(filter(lambda promo: promo != '', promos)):
            if promo == '1':
                all_promos.append({ 'id': '1', 'name': 'Weekly Specials' })
            elif promo == '2':
                all_promos.append({ 'id': '2', 'name': 'Daily Deals' })
            elif promo == '13':
                all_promos.append({ 'id': '12', 'name': 'One Day Sale' })
            elif promo == '13':
                all_promos.append({ 'id': '13', 'name': 'Staff Picks' })
            elif promo == '14':
                all_promos.append({ 'id': '14', 'name': 'Weekend Sale' })
            elif promo == '17':
                all_promos.append({ 'id': '17', 'name': 'Upcoming Pre-Order Deadline' })
            elif promo == '21':
                all_promos.append({ 'id': '21', 'name': '' })
            elif promo == '31':
                all_promos.append({ 'id': '31', 'name': 'Spotlight' })
            elif promo == '35':
                all_promos.append({ 'id': '35', 'name': 'Plus More' })
            elif promo == '43':
                all_promos.append({ 'id': '43', 'name': 'Figure Clearance' })
            else:
                all_promos.append({ 'id': promo, 'name': 'Unknown' })
        return all_promos

    def get_sales(self, sales: List[str]) -> List[ISale]:
        all_sales = []
        for sale in list(filter(lambda sale: sale != '', sales)):
            if sale == '1':
                all_sales.append({ 'id': '1', 'name': 'Everything On Sale' })
            elif sale == '2':
                all_sales.append({ 'id': '2', 'name': 'Newly Added' })
            elif sale == '3':
                all_sales.append({ 'id': '3', 'name': 'Today\'s Mega Deal' })
            elif sale == '4':
                all_sales.append({ 'id': '4', 'name': 'Viz Media Weekly Specials' })
            elif sale == '12':
                all_sales.append({ 'id': '12', 'name': 'Cyber Monday' })
            elif sale == '16':
                all_sales.append({ 'id': '16', 'name': 'Got  Anime Early Access' })
            elif sale == '21':
                all_sales.append({ 'id': '21', 'name': 'Bundle Savings' })
            elif sale == '32':
                all_sales.append({ 'id': '32', 'name': 'Vender Spotlight' })
            elif sale == '35':
                all_sales.append({ 'id': '35', 'name': 'Week 1' })
            elif sale == '36':
                all_sales.append({ 'id': '36', 'name': 'Week 2' })
            elif sale == '37':
                all_sales.append({ 'id': '37', 'name': 'Week 3' })
            elif sale == '38':
                all_sales.append({ 'id': '38', 'name': 'Week 4' })
            elif sale == '45':
                all_sales.append({ 'id': '45', 'name': 'Yen Press Specials' })
            elif sale == '48':
                all_sales.append({ 'id': '48', 'name': 'Staff Picks' })
            else:
                all_sales.append({ 'id': sale, 'name': 'Unknown' })
        return all_sales

    def get_stock_status(self, is_in_stock: bool, is_pre_order: bool, is_purchasable: bool):
        if is_in_stock:
            return 'In Stock'
        if is_pre_order:
            return 'Pre-Order'
        if is_purchasable:
            return 'Out of Stock'
        return 'Out of Print'

    def get_rating_bucket(self, rating: str):
        if rating == 'ALL':
            return 'A – All Ages'
        try:
            r_bucket = int(rating[:-1])
        except:
            return 'Unknown'
        if r_bucket <= 10:
            return 'A – All Ages'
        if r_bucket <= 13:
            return 'T – Teen'
        if r_bucket <= 16:
            return 'OT – Older Teen'
        return 'M – Mature'

    def get_item_id(self, item: IRightStufItem):
        if 'BUNDLE' in item.itemid:
            return item.itemid
        else:
            item_id = re.sub('[^0-9]', '', item.itemid)
            if len(item_id) < 13:
                self.logger.warning('incorrectly formatted id: ' + item.itemid)
            return item_id
        
    def get_format(self, item: IRightStufItem):
        if 'BUNDLE' in item.itemid:
            return FormatEnum.BUNDLE.value
        if 'Box Set' in item.displayname or 'Box Set' in item.storedisplayname2:
            return FormatEnum.BOXSET.value
        if item.custitem_rs_web_class == FormatEnum.MANGA.value:
            return FormatEnum.MANGA.value
        if item.custitem_rs_web_class == FormatEnum.NOVEL.value or item.custitem_rs_web_class == 'Novels':
            return FormatEnum.NOVEL.value
        if item.custitem_rs_web_class == FormatEnum.MANHWA.value:
            return FormatEnum.MANHWA.value
        if item.custitem_rs_web_class == FormatEnum.MANHUA.value:
            return FormatEnum.MANHUA.value
        self.logger.warning('Invalid format found for ' + item.itemid + ' ' + item.urlcomponent)
        return ''
        
    def get_bundle_volumes(self, item: IVolume):
        try:
            series: dict[str:ISeries] = self.local_dao.get_json_file(FilePathEnum.SERIES.value[self.host])
            series_list: List[ISeries] = list(series.values())
            bundle = re.search('\(\d\-\d\) Bundle', item.display_name).group(0).split('-')
            volumes = [str(vol) for vol in list(range(int(bundle[0][1:]), int(bundle[1].split(')')[0])))]
            for s in series_list:
                if s.title == item.series:
                    series_volumes = { series_volume.volume : series_volume.isbn for series_volume in s.volumes }
                    item.contained_isbns = [series_volumes.get(volume) for volume in volumes]
        except:
            self.logger.error('Could not get volumes in the bundle - ' + item.display_name + ' | ' + item.series, traceback.format_exc())

    def unpack_item(self, item: IRightStufItem, all_items: List[IVolume]) -> Tuple[str, IVolume]:
        item_id = self.get_item_id(item)
        now = self.common_helper.get_timezone_now()
        if item_id not in all_items:
            enriched_item = IVolume()
            enriched_item.record_added_date = now
            enriched_item.last_stock_update = now
        else:
            enriched_item = IVolume(all_items[item_id])
        enriched_item.record_updated_date = now

        # volume details
        enriched_item.isbn = item_id
        enriched_item.display_name = item.displayname if item.displayname else item.storedisplayname2
        enriched_item.format = self.get_format(item)
        enriched_item.name = self.parse_name(
            enriched_item.display_name,
            'Novel' if item.custitem_rs_web_class == 'Novels' else item.custitem_rs_web_class
        ).title()
        enriched_item.volume = self.parse_volume(enriched_item.display_name, enriched_item.format)
        enriched_item.cover_images = self.get_cover_images(item_id, item.itemimages_detail, enriched_item.display_name)
        enriched_item.series = item.custitem_rs_series
        enriched_item.artist = item.custitem_rs_artist
        enriched_item.author = item.custitem_rs_author
        enriched_item.description = item.storedetaileddescription.replace('<p>', '').replace('</p>', '')
        enriched_item.genres = list(filter(lambda genre: genre != '&nbsp;', item.custitem_rs_genre.split(', ')))
        enriched_item.themes = list(filter(lambda theme: theme != '&nbsp;', item.custitem_rs_themes.split(', ')))
        enriched_item.publisher = ' '.join([s.capitalize() for s in item.custitem_rs_publisher.split(' ')])
        enriched_item.age_rating = item.custitem_rs_age_rating
        enriched_item.age_rating_bucket = self.get_rating_bucket(item.custitem_rs_age_rating)
        enriched_item.page_count = item.custitem_rs_page_count
        enriched_item.adult = item.custitem_rs_adult
        enriched_item.weight = item.weight
        enriched_item.internal_id = item.internalid
        enriched_item.url_component = item.urlcomponent

        # item status
        enriched_item.is_in_stock = item.isinstock
        enriched_item.is_purchasable = item.ispurchasable
        enriched_item.is_pre_order = item.custitem_rs_new_releases_preorders == 'Pre-order'
        enriched_item.is_backorderable = item.isbackorderable

        new_stock_status = self.get_stock_status(enriched_item.is_in_stock, enriched_item.is_pre_order, enriched_item.is_purchasable)
        if new_stock_status != enriched_item.stock_status:
            enriched_item.last_stock_update = now
        enriched_item.stock_status = new_stock_status
        
        enriched_item.is_on_sale = self.is_on_sale(item.custitem_rs_current_sale_ids)
        enriched_item.promos = self.get_promos(json.loads(item.custitem_rs_current_sale_ids).get('specialsAndPromosIds'))
        enriched_item.sales = self.get_sales(json.loads(item.custitem_rs_current_sale_ids).get('sales'))
        enriched_item.publisher_backorder = item.custitem_rs_publisher_backorder
        enriched_item.image_not_final = item.custitem_rs_image_not_final
        enriched_item.condition = item.custitem_damaged_type
        enriched_item.exclude_free_shipping = item.custitem_rs_exclude_free_shipping

        # prices
        enriched_item.retail_price = item.pricelevel1
        enriched_item.non_member_price = item.pricelevel5
        enriched_item.member_price = item.pricelevel2
        enriched_item.price_lvl_3 = item.pricelevel3

        # dates
        enriched_item.release_date = item.custitem_rs_release_date
        enriched_item.reprint_date = item.custitem_rs_reprint_date
        enriched_item.pre_book_date = item.custitem_rs_pre_book_date

        if enriched_item.format == FormatEnum.BUNDLE.value:
            self.get_bundle_volumes(item)

        return (item_id, enriched_item)

