"""Models for Manga Inventory DB"""
import uuid
from datetime import datetime
from sqlalchemy import UUID, Column, Integer, String, Date, DateTime, Float, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from .database_connection import db

class MangaRecord(db.Model):
    """DB Model for a Manga Record containing its information for each isbn
    Key: isbn
    
    Track By
    - record_added_date
    - record_updated_date
    """

    isbn = Column(String, primary_key=True)
    record_added_date = Column(DateTime)
    record_updated_date = Column(DateTime)

    name = Column(String)
    format = Column(String)
    volume = Column(String)
    primary_cover_image_url = Column(String)
    other_images = Column(mutable_json_type(dbtype=JSONB, nested=True))
    series = Column(String)
    artist = Column(String)
    author = Column(String)
    description = Column(String)
    genres = Column(mutable_json_type(dbtype=JSONB, nested=True))
    themes = Column(mutable_json_type(dbtype=JSONB, nested=True))
    publisher = Column(String)
    age_rating = Column(String)
    age_rating_bucket = Column(String)
    page_count = Column(Integer)
    adult = Column(Boolean)
    weight = Column(Float)
    url_component = Column(String)
    image_not_final = Column(Boolean)
    retail_price = Column(Float)
    release_date = Column(Date)
    reprint_date = Column(Date)
    pre_book_date = Column(String)
    series_id = Column(String)
    edition_id = Column(String)

    def to_dict(self):
        """Convert MangaRecord model into a dict form for python.
        """
        today_datetime = datetime.today().date()
        return {
            'isbn': self.isbn,
            'record_added_date': str(self.record_added_date.strftime('%Y-%m-%d %H:%M:%S')) \
                if self.record_added_date else today_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'record_updated_date': str(self.record_updated_date.strftime('%Y-%m-%d %H:%M:%S')) \
                if self.record_updated_date else today_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'name': self.name,
            'format': self.format,
            'volume': self.volume,
            'primary_cover_image_url': self.primary_cover_image_url,
            'other_images': self.other_images,
            'series': self.series,
            'artist': self.artist,
            'author': self.author,
            'description': self.description,
            'genres': self.genres,
            'themes': self.themes,
            'publisher': self.publisher,
            'age_rating': self.age_rating,
            'age_rating_bucket': self.age_rating_bucket,
            'page_count': self.page_count,
            'adult': self.adult,
            'weight': self.weight,
            'url_component': self.url_component,
            'image_not_final': self.image_not_final,
            'retail_price': self.retail_price,
            'release_date': str(self.release_date.strftime('%Y-%m-%d')) \
                if self.release_date else None,
            'reprint_date': str(self.reprint_date.strftime('%Y-%m-%d')) \
                if self.reprint_date else None,
            'pre_book_date': self.pre_book_date \
                if self.pre_book_date else None,
            'series_id': self.series_id,
            'edition_id': self.edition_id
        }


class StoreRecord(db.Model):
    """DB Model for a Store Record containing a store item that correlates to an isbn.
    Multiple stores can have multiple records of one isbn. The price and condition details
    are kept here.
    Key: id as UUID
    
    Track By
    - record_added_date
    - record_updated_date
    """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_added_date = Column(DateTime)
    record_updated_date = Column(DateTime)

    isbn = Column(String)
    store_id = Column(String)
    store_name = Column(String)
    store_icon_url = Column(String)
    is_in_stock = Column(Boolean)
    is_purchasable = Column(Boolean)
    is_pre_order = Column(Boolean)
    is_backorderable = Column(Boolean)
    stock_status = Column(String)
    is_on_sale = Column(Boolean)
    last_stock_update = Column(DateTime)
    publisher_backorder = Column(Boolean)
    condition = Column(String)
    exclude_free_shipping = Column(Boolean)
    price = Column(Float) # current price (may be discount)
    member_price = Column(Float)

    def to_dict(self):
        """Convert MangaRecord model into a dict form for python.
        """
        return {
            'id': self.id,
            'record_added_date': str(self.record_added_date.strftime('%Y-%m-%d %H:%M:%S')) \
                if self.record_added_date else None,
            'record_updated_date': str(self.record_updated_date.strftime('%Y-%m-%d %H:%M:%S')) \
                if self.record_updated_date else None,
            'isbn': self.isbn,
            'store_id': self.store_id,
            'store_name': self.store_name,
            'store_icon_url': self.store_icon_url,
            'is_in_stock': self.is_in_stock,
            'is_purchasable': self.is_purchasable,
            'is_pre_order': self.is_pre_order,
            'is_backorderable': self.is_backorderable,
            'stock_status': self.stock_status,
            'is_on_sale': self.is_on_sale,
            'last_stock_update': str(self.last_stock_update.strftime('%Y-%m-%d %H:%M:%S')) \
                if self.last_stock_update else None,
            'publisher_backorder': self.publisher_backorder,
            'condition': self.condition,
            'exclude_free_shipping': self.exclude_free_shipping,
            'price': self.price,
            'member_price': self.member_price
        }
