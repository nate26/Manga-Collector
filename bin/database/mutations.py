"""GQL Mutations to modify data in the DB"""
import json
from typing import Dict
from database.models import MangaRecord
from .database_connection import db

def create_manga_resolver(_obj, _info, manga_input: Dict):
    """Create a new manga record in the DB"""
    try:
        manga_record = MangaRecord(**manga_input)
        db.session.add(manga_record)
        db.session.commit()
        payload = {
            "success": True,
            "manga_record": manga_record.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect manga record format provided " + json.dumps(manga_record)]
        }
    return payload

def update_manga_resolver(_obj, _info, m_id: str, manga_update: Dict):
    """Update an existing manga record in the DB"""
    try:
        existing = MangaRecord.query.get(m_id)
        if existing:
            for key, val in manga_update.items():
                setattr(existing, key, val)
            db.session.add(existing)
            db.session.commit()
            payload = {
                "success": True,
                "manga_record": existing.to_dict()
            }
        else:
            payload = {
                "success": False,
                "errors": ["Manga Record by ID " + m_id + " does not exist..."]
            }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect manga record format provided " + json.dumps(manga_update)]
        }
    return payload

def delete_manga_resolver(_obj, _info, m_id: str):
    """Delete an existing manga record in the DB"""
    try:
        manga_record = MangaRecord.query.get(m_id)
        if manga_record:
            db.session.delete(manga_record)
            db.session.commit()
            payload = {
                "success": True
            }
        else:
            payload = {
                "success": False,
                "errors": ["Manga Record by ID " + m_id + " does not exist..."]
            }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Could not delete manga record by ID " + m_id]
        }
    return payload
