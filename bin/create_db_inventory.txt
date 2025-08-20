"""Create table and insert into table"""
from datetime import datetime
from enums.file_path_enum import FilePathEnum
from enums.host_enum import HostEnum
from util.local_dao import LocalDAO
from database.models import MangaRecord
from database.database_connection import app, db
from sqlalchemy import inspect

with app.app_context():
    db.create_all()

    # Check existing table names
    inspector = inspect(db.engine)
    print([{ 'schema': schema, 'tables': inspector.get_table_names(schema=schema) } \
        for schema in inspector.get_schema_names()])

    local_dao = LocalDAO(HostEnum.MOCK)
    data = list(local_dao.get_json_file(FilePathEnum.ALL_ITEMS.value[HostEnum.MOCK.value])
                .get('items').values())
    for manga in data[0:30]:
        images = manga.get('cover_images')
        primary_cover_image_url = \
            list(filter(lambda x: x.get('name') == 'primary', images))[0].get('url') \
            if 'primary' in [image.get('name') for image in images] \
            else images[-1].get('url') if len(images) > 0 else None
        new_manga = MangaRecord(
            isbn = manga.get('isbn'),
            record_added_date = datetime.strptime(manga.get('record_added_date'), \
                '%Y-%m-%d %H:%M:%S'),
            record_updated_date = datetime.strptime(manga.get('record_updated_date'), \
                '%Y-%m-%d %H:%M:%S'),
            name = manga.get('name'),
            format = manga.get('format'),
            volume = manga.get('volume'),
            primary_cover_image_url = primary_cover_image_url.replace('www', 'legacy') \
                if primary_cover_image_url else None,
            other_images = [ \
                {
                    'name': image.get('name'),
                    'url': image.get('url').replace('www', 'legacy')
                }
                for image
                in list(filter(lambda x: x.get('url') != primary_cover_image_url, images))
            ],
            series = manga.get('series'),
            artist = manga.get('artist'),
            author = manga.get('author'),
            description = manga.get('description'),
            genres = manga.get('genres'),
            themes = manga.get('themes'),
            publisher = manga.get('publisher'),
            age_rating = manga.get('age_rating'),
            age_rating_bucket = manga.get('age_rating_bucket'),
            page_count = manga.get('page_count'),
            adult = manga.get('adult'),
            weight = manga.get('weight'),
            url_component = manga.get('url_component'),
            image_not_final = manga.get('image_not_final'),
            retail_price = manga.get('retail_price'),
            release_date = datetime.strptime(manga.get('release_date'), '%m/%d/%Y').date() \
                if manga.get('release_date') else None,
            reprint_date = datetime.strptime(manga.get('reprint_date'), '%m/%d/%Y').date() \
                if manga.get('reprint_date') else None,
            pre_book_date = datetime.strptime(manga.get('pre_book_date'), '%m/%d/%Y').date() \
                if manga.get('pre_book_date') else None,
            series_id = manga.get('series_id'),
            edition_id = manga.get('edition_id')
        )
        db.session.add(new_manga)
    db.session.commit()
    records = MangaRecord.query.all()
    print(records)
