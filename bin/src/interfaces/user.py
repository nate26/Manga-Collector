'''Interface for User data'''

from typing import List

class UserProfile(dict):
    '''User profile settings'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    picture: str | None
    banner: str | None
    color: str | None
    theme: str | None

class User(dict):
    '''User data'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    id: str
    username: str
    password: bytes
    user_id: str
    profile: UserProfile
    personal_stores: List[str]
