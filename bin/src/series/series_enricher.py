from typing import Tuple
import uuid
from datetime import datetime
from interfaces.iseries import ISeriesVolume
from interfaces.iseries import IEdition, ISeries
from enums.format_enum import FormatEnum
from interfaces.ivolume import IVolume

from util.manga_logger import MangaLogger

class SeriesEnricher:

    def __init__(self, host):
        self.logger = MangaLogger(host, __name__)
        
    def get_edition_name(self, item: IVolume):
        if item.series in item.display_name:
            edition_name = item.display_name.rsplit('Volume', 1)[0].rsplit(item.volume)[0] \
                if ('Volume ' + str(item.volume)) in item.display_name \
                else item.display_name
            if item.format in (FormatEnum.MANGA.value, FormatEnum.MANHUA.value, FormatEnum.MANHWA.value, FormatEnum.NOVEL.value):
                edition_name = edition_name.rsplit(item.format, 1)[0]
            return edition_name.strip()
        return item.series

    def update_series(self, item: IVolume, series: dict[str:ISeries]) -> Tuple[str, ISeries, str]:
        title = item.series
        edition_name = self.get_edition_name(item)
        if item.volume is None:
            item.volume = '1'
        series_titles = [ISeries(s).title for s in list(series.values())]
        if title not in series_titles:
            # scenario: new series
            series_id = str(uuid.uuid4())
            edition_id = str(uuid.uuid4())
            series_update: ISeries = {
                'title': title,
                'series_id': series_id,
                'editions': {
                    edition_id: {
                        'edition': edition_name,
                        'edition_id': edition_id,
                        'format': item.format,
                        'volumes': [
                            ISeriesVolume({
                                'isbn': item.isbn,
                                'volume': item.volume,
                                'release_date': item.release_date
                            })
                        ]
                    }
                }
            }
        else:
            # scenario: existing series
            series_id = str(list(series.keys())[series_titles.index(title)])
            series_update = ISeries(series[series_id])
            f_edition = [IEdition(e) for e in list(series_update.editions.values())
                         if edition_name == IEdition(e).edition and item.format == IEdition(e).format]
            if len(f_edition) > 0:
                edition_update = IEdition(f_edition[0])
                edition_id = edition_update.edition_id
                # scenario: existing edition
                if item.isbn not in [ISeriesVolume(vol).isbn for vol in edition_update.volumes]:
                    # scenario: add to series
                    edition_update.volumes.append({
                        'isbn': item.isbn,
                        'volume': item.volume, 
                        'release_date': item.release_date
                    })
                else:
                    # scenario: update release date
                    idx = list([ISeriesVolume(v).isbn for v in edition_update.volumes]).index(item.isbn)
                    edition_update.volumes[idx] = ISeriesVolume({
                        'isbn': item.isbn,
                        'volume': item.volume,
                        'release_date': item.release_date
                    })
                # sorts the updated array of volumes by release date
                edition_update.volumes.sort(
                    key=lambda x:
                        datetime.strptime(x.get('release_date'), "%m/%d/%Y")
                        if x.get('release_date') != ''
                        else '',
                    reverse=False
                )
                # updates the edition in the series
                series_update.editions[edition_update.edition_id] = edition_update
            else:
                # scenario: new edition
                edition_id = str(uuid.uuid4())
                series_update.editions[edition_id] = {
                    'edition': edition_name,
                    'edition_id': edition_id,
                    'format': item.format,
                    'volumes': [
                        ISeriesVolume({
                            'isbn': item.isbn,
                            'volume': item.volume,
                            'release_date': item.release_date
                        })
                    ]
                }
        return (series_id, series_update, edition_id)
