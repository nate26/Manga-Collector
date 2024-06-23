'''Auth class to generate and decode JWT token'''

import secrets
from datetime import datetime, timezone, timedelta
import jwt

from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

class Auth:
    '''
    A class used to generate and decode JWT token
    
    ...

    Parameters
    ----------
    host : HostEnum
        The the host machine to know where to access data for logging
    
    Attributes
    ----------
    logger : MangaLogger
        a logging utility for info, warning, and error logs
    
    Methods
    -------
    generate_token(username: str, password: str)
        Generates a JWT token
    encode(body: dict, secret: str)
        Encodes a JWT token
    decode(encoded_jwt: str, secret: str)
        Decodes a JWT token
    '''

    def __init__(self, host: HostEnum):
        self.logger = MangaLogger(host).register_logger(__name__)
        self.pass_key = ''

    def generate_secret(self):
        '''
        Generates a JWT token for the given user
        
        Parameters:
        - username (str): The username to be encoded in the JWT token
        - password (str): The password to be encoded in the JWT token
        '''
        return secrets.token_urlsafe(32)

    def encode(self, body: dict, secret: str) -> str:
        '''
        Encodes a JWT token with the given body and secret
        
        Parameters:
        - body (dict): The body of the JWT token
        - secret (str): The secret to encode the JWT token
        
        Returns:
        - str: The encoded JWT token
        '''
        return jwt.encode(
            {
                'username': body['username'],
                'exp': datetime.now(tz = timezone.utc) + timedelta(minutes=30)
            },
            secret,
            algorithm="HS256"
        )

    def decode(self, encoded_jwt: str, secret: str):
        '''
        Decodes a JWT token with the given encoded JWT token and secret
        
        Parameters:
        - encoded_jwt (str): The encoded JWT token
        - secret (str): The secret to decode the JWT token
        
        Returns:
        - dict: The decoded JWT token
        '''
        return jwt.decode(encoded_jwt, secret, algorithms=["HS256"])

    def authenticate(self, body):
        '''
        Authenticates a user with the given body
        
        Parameters:
        - body (dict): The body with the username and password
        
        Returns:
        - bool: True if the user is authenticated, False otherwise
        '''
        return body['username'] == 'admin' and body['password'] == 'admin'
