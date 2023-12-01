"""GQL Queries to get data from the DB"""
from database.models import MangaRecord

def list_manga_records_resolver(_obj, _info):
    """Gets a list of all manga records from the DB"""
    try:
        manga_records = [manga_record.to_dict() for manga_record in MangaRecord.query.all()]
        print(manga_records)
        payload = {
            "success": True,
            "manga_records": manga_records
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

# @convert_kwargs_to_snake_case
def get_manga_record_resolver(_obj, _info, m_id: str):
    """Gets a single manga record by its ID from the DB"""
    try:
        manga_record = MangaRecord.query.get(m_id)
        payload = {
            "success": True,
            "manga_record": manga_record.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["MangaRecord item matching {id} not found"]
        }
    return payload
