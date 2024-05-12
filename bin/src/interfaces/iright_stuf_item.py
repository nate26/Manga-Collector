from typing import Any


class IRightStufPriceDetail:
    onlinecustomerprice_formatted: str = None
    onlinecustomerprice: float = None


class IRightStufItem:
    
    def __init__(self, obj={}):
        for key in obj:
            setattr(self, key, obj[key])
            
    custitem_rs_spoken_language: str = None
    custitem_hide_from_website: bool = None
    custitem_rs_genre: str = None
    custitem_ns_pr_item_attributes: str = None
    searchkeywords: str = None
    custitem_rs_current_sale_ids: str = None
    custitem_rs_top_selling_item: bool = None
    custitem_rs_reprint_date: str = None
    ispurchasable: bool = None
    custitem_rs_adult: bool = None
    custitem_ns_pr_attributes_rating: str = None
    custitem_rs_themes: str = None
    custitem_rs_image_not_final: bool = None
    stockdescription: str = None
    custitem_rs_availabe_for_purchase: bool = None
    pricelevel2_formatted: str = None
    storedetaileddescription: str = None
    itemimages_detail: dict[str:dict] = None
    custitem_rs_exclude_free_shipping: bool = None
    onlinecustomerprice_detail: IRightStufPriceDetail = None
    weight: float = None
    custitem_ns_pr_rating_by_rate: str = None
    pricelevel5_formatted: str = None
    custitem_rs_youtube_trailer: str = None
    custitem_rs_vimeo_trailer: str = None
    internalid: float = None
    custitem2: str = None
    custitem_rs_publisher: str = None
    itemoptions_detail: Any = None
    outofstockmessage: str = None
    custitem_rs_new_releases_preorders: str = None
    custitem1: str = None
    relateditemsdescription: str = None
    pricelevel1_formatted: str = None
    custitem_rs_series: str = None
    isinstock: bool = None
    custitem_rs_release_date: str = None
    custitem_rs_web_class: str = None
    custitem_rs_publisher_backorder: bool = None
    metataghtml: str = None
    custitem_in_stock: bool = None
    custitem_rs_artist: str = None
    itemid: str = None
    custitem_rs_age_rating: str = None
    custitem_rs_discount_exclude: bool = None
    custitem_rs_scale: str = None
    isbackorderable: str = None
    custitem_rs_figure_type: str = None
    custitem_rs_subtitle_language: str = None
    custitem_rs_page_count: float = None
    pricelevel3_formatted: str = None
    showoutofstockmessage: bool = None
    outofstockbehavior: str = None
    itemtype: str = None
    custitem_damaged_type: str = None
    pricelevel5: float = None
    pricelevel3: float = None
    displayname: str = None
    storedisplayname2: str = None
    pricelevel2: float = None
    custitem_rs_pre_book_date: str = None
    custitem_rs_vimeo_trailer_2: str = None
    pricelevel1: float = None
    custitem_rs_vimeo_trailer_3: str = None
    pagetitle: str = None
    custitem_rs_author: str = None
    custitem_rs_specialty_product: str = None
    urlcomponent: str = None