import traceback
from interfaces.icollection import ICollectionDisplay
from interfaces.ilibrary import ILibraryItem
from interfaces.iseries import IEdition, ISeries, IEditionEnriched
from src.data import Data
from typing import Dict, List
from util.manga_logger import MangaLogger

class Collection:
    

    def __init__(self, host):
        self.data = Data(host)
        self.logger = MangaLogger(host, __name__)

    def enrich_edition(self, edition: IEdition, items_db: List[ILibraryItem]) -> IEditionEnriched:
        return {
            'edition': edition.get('edition'),
            'edition_id': edition.get('edition_id'),
            'format': edition.get('format'),
            'volumes': [items_db.get(vol.get('isbn')) for vol in edition.get('volumes')]
        }

    def get_collection(self, user_id: str):
        collection_db = self.data.get_collection_data(user_id)
        items_db = self.data.get_library_data().get('items')
        series_db = self.data.get_series_data()
        collection_by_vol: List[str] = []
        collection_by_series: List[str] = []
        collection_by_edition: List[str] = []
        collection_vol_data: Dict[str, ICollectionDisplay] = {}
        collection_series_data: Dict[str, ISeries] = {}
        for item in collection_db:
            isbn = item.get('isbn')

            try:
                item_data = items_db.get(isbn)
                series_id = item_data.get('series_id')
                edition_id = item_data.get('edition_id')
                try:
                    series_data = series_db.get(series_id)
                    edition_data = self.enrich_edition(series_data.get('editions').get(edition_id), items_db)
                except:
                    self.logger.error('Error getting Series data for ' + series_id, traceback.format_exc())
            except:
                self.logger.error('Error getting Item data for ' + isbn, traceback.format_exc())

            if item_data != None and series_data != None:

                collection_by_vol.append(isbn)

                if series_id not in collection_by_series:
                    collection_by_series.append(series_id)

                if edition_id not in collection_by_edition:
                    collection_by_edition.append(edition_id)

                if isbn not in collection_vol_data:
                    collection_vol_data[isbn] = { **item, **item_data }

                if series_id not in collection_series_data:
                    # add new series
                    collection_series_data[series_id] = {
                        'title': series_data.get('title'),
                        'series_id': series_data.get('series_id'),
                        'editions': { edition_id: edition_data }
                    }
                elif edition_id not in collection_series_data.get(series_id).get('editions'):
                    # add to existing series
                    collection_series_data[series_id] = {
                        'title': series_data.get('title'),
                        'series_id': series_data.get('series_id'),
                        'editions': {
                            **{ edition_id: edition_data },
                            **{
                                id:self.enrich_edition(edition, items_db)
                                for (id, edition)
                                in collection_series_data.get(series_id).get('editions').items()
                            }
                        }
                    }

            else:
                # add item when data could not be found
                collection_by_vol.append(isbn)
                collection_vol_data[isbn] = item
                self.logger.warning('Providing item from collection that could not be found in item data or series ' + isbn)

        return {
            'lists': {
                'volumes': collection_by_vol,
                'series': collection_by_series,
                'editions': collection_by_edition
            },
            'ref': {
                'volume_data': collection_vol_data,
                'series_data': collection_series_data
            }
        }