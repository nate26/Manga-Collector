'''Auth class to generate and decode JWT token'''

import json
from datetime import datetime, timezone, timedelta
import uuid
import bcrypt
import jwt

from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.interfaces.user import User
from src.util.local_dao import LocalDAO
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
        self.host = host
        self.logger = MangaLogger(host).register_logger(__name__)
        self.local_dao = LocalDAO(host)

        vault = self.local_dao.open_file(FilePathEnum.VAULT.value[self.host.value])
        self.secret = vault['secret']
        self.refresh_secret = vault['refresh_secret']
        self.password_salt = bytes(vault['password_salt'], 'utf-8')

    def decode_user(self, encoded_jwt: str):
        '''
        Decodes a JWT token with the given encoded JWT token and secret
        
        Parameters:
        - encoded_jwt (str): The encoded JWT token
        - secret (str): The secret to decode the JWT token
        
        Returns:
        - dict: The decoded JWT token
        '''
        try:
            decoded = jwt.decode(encoded_jwt, self.secret, algorithms=["HS256"])
            self.logger.info('User has been authenticated')
            return decoded
        except jwt.ExpiredSignatureError:
            self.logger.error('Token has expired')
            return None
        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, ValueError):
            self.logger.error('Token is invalid')
            return None

    def __encode(self, username: str, secret: str) -> dict[str, str | float]:
        '''
        Encodes a JWT token with the given body and secret
        
        Parameters:
        - username (str): Username for the body of the JWT token
        - secret (str): The secret to encode the JWT token
        
        Returns:
        - str: The encoded JWT token
        '''
        expiration = datetime.now(tz = timezone.utc) + timedelta(minutes=30)
        return {
            "token": jwt.encode(
                {
                    'username': username,
                    'exp': expiration
                },
                secret
            ),
            "expiration": expiration.timestamp(),
            "refresh_token": jwt.encode(
                { 'username': username },
                self.refresh_secret
            )
        }

    def __validate_input(self, input_text: str, password=False):
        '''
        Validates the input
        
        Parameters:
        - input (str): The input to validate
        
        Returns:
        - bool: True if the input is valid, False otherwise
        '''
        return input_text and isinstance(input_text, str) and \
            (len(input_text) > 8 if password else len(input_text) > 3)

    def login(self, body):
        '''
        Log in authentication for the user with the given body.
        Will not log in if the email / password was invalid or the user does not exist.
        
        Parameters:
        - body (dict): The body with the email and password
        
        Returns:
        - str: The encoded JWT token
        
        Exceptions:
        - ValueError: If the password is missing or not a string
        - FileNotFoundError: If the file is not found
        - json.JSONDecodeError: If the JSON file has an error
        '''
        try:
            self.__validate_input('email', body['email'])
            self.__validate_input('password', body['password'])
        except ValueError as e:
            self.logger.error('Failed to validate input %s', e)
            raise e

        try:
            all_users: dict[str, User] = self.local_dao.open_file(
                FilePathEnum.USERS.value[self.host.value]
            )

            email = body['email']
            if email not in all_users:
                raise ValueError('There is no account with this email... please sign in.')

            password_hash = str(bcrypt.hashpw(body['password'].encode('utf-8'), self.password_salt))
            if all_users[email]['password'] != password_hash:
                raise ValueError('Password is incorrect')

            authentication = self.__encode(all_users[email]['username'], self.secret)
            return {
                "email": all_users[email]['email'],
                "username": all_users[email]['username'],
                "user_id": all_users[email]['user_id'],
                "profile": {
                    **all_users[email]['profile']
                },
                "personal_stores": all_users[email]['personal_stores'],
                "authentication": {
                    **authentication
                }
            }

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.error('Failed to login user %s', e)
            raise e

    def sign_up(self, body):
        '''
        Signs up a user with the given body, setting the new user into the user DB.
        Provides the user with a JWT token
        
        Parameters:
        - body (dict): The body with the username and password
        
        Returns:
        - str: The encoded JWT token
        
        Exceptions:
        - ValueError: If the password is missing or not a string
        - FileNotFoundError: If the file is not found
        - json.JSONDecodeError: If the JSON file has an error
        '''
        try:
            self.__validate_input('email', body['email'])
            self.__validate_input('username', body['username'])
            self.__validate_input('password', body['password'])
        except ValueError as e:
            self.logger.error('Failed to validate input %s', e)
            raise e

        try:
            all_users: dict[str, User] = self.local_dao.open_file(
                FilePathEnum.USERS.value[self.host.value]
            )

            email = body['email']
            if email in all_users:
                raise ValueError('There is already an account with this email... please login.')

            password_hash = str(bcrypt.hashpw(body['password'].encode('utf-8'), self.password_salt))
            all_users[email] = User({
                'email': body['email'],
                'username': body['username'],
                'password': password_hash,
                'user_id': str(uuid.uuid4()),
                'profile': {
                    'picture': None,
                    'banner': None,
                    'color': None,
                    'theme': None
                },
                'personal_stores': []
            })
            self.local_dao.save_file(FilePathEnum.USERS.value[self.host.value], all_users)

            authentication = self.__encode(all_users[email]['username'], self.secret)
            return {
                "email": all_users[email]['email'],
                "username": all_users[email]['username'],
                "user_id": all_users[email]['user_id'],
                "profile": {
                    **all_users[email]['profile']
                },
                "personal_stores": all_users[email]['personal_stores'],
                "authentication": {
                    **authentication
                }
            }

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.error('Failed to sign up user %s', e)
            raise e
