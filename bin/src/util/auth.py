"""Auth class to generate and decode JWT token"""

import json
from datetime import datetime, timezone, timedelta
import re
import uuid
import bcrypt
import jwt

from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.interfaces.user import User
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class Auth:
    """
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
    """

    def __init__(self, host: HostEnum):
        self.host = host
        self.logger = MangaLogger(host).register_logger(__name__)
        self.local_dao = LocalDAO(host)

        vault = self.local_dao.open_file(FilePathEnum.VAULT.value[self.host.value])
        self.secret = vault["secret"]
        self.refresh_secret = vault["refresh_secret"]
        self.password_salt = bytes(vault["password_salt"], "utf-8")

    def decode_user(self, encoded_jwt: str, secret: str):
        """
        Decodes a JWT token with the given encoded JWT token and secret

        Parameters:
        - encoded_jwt (str): The encoded JWT token
        - secret (str): The secret to decode the JWT token

        Returns:
        - dict: The decoded JWT token
        """
        try:
            decoded = jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
            self.logger.info("User has been authenticated")
            return decoded
        except jwt.ExpiredSignatureError:
            self.logger.error("Token has expired")
            return None
        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, ValueError):
            self.logger.error("Token is invalid")
            return None

    def __encode(self, username: str, secret: str) -> dict[str, str | float]:
        """
        Encodes a JWT token with the given body and secret

        Parameters:
        - username (str): Username for the body of the JWT token
        - secret (str): The secret to encode the JWT token

        Returns:
        - str: The encoded JWT token
        """
        expiration = datetime.now(tz = timezone.utc) + timedelta(minutes=30)
        return {
            "token": jwt.encode(
                {
                    "username": username,
                    "exp": expiration
                },
                secret
            ),
            "expiration": expiration.timestamp(),
            "refresh_token": jwt.encode(
                { "username": username },
                self.refresh_secret
            )
        }

    def __validate_input(self, input_type: str, input_text: str):
        """
        Validates the input

        Parameters:
        - input (str): The input to validate

        Returns:
        - bool: True if the input is valid, False otherwise
        """
        if input_type == "email" and isinstance(input_text, str) and not re.match((
            '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)'
            '*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\'
            '[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])'
            '?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])'
            '|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]'
            '|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-'
            '\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\\])'
        ), input_text):
            raise ValueError("Email is not valid")

        if input_type == "username" and isinstance(input_text, str) and len(input_text) < 4:
            raise ValueError("Username must be at least 4 characters long")

        if input_type == "password" and isinstance(input_text, str) and not re.match((
            '(?=.*[A-Za-z])(?=.*[0-9])'
            '(?=.*[$@$!#^~%*?&,.<>"\'\\;:{\\}\\[\\]\\|\\+\\-\\=\\_\\)\\(\\)\\`\\/\\\\\\]])'
            '[A-Za-z0-9d$@].{8,}'
        ), input_text):
            raise ValueError("Password must be at least 8 characters long with at least "
                             "1 capital letter, 1 number, and 1 special character")

    def login(self, _obj, _info, email: str, password: str):
        """
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
        """
        try:
            self.__validate_input("email", email)
            self.__validate_input("password", password)
        except ValueError as e:
            self.logger.error("Failed to validate input %s", e)
            raise e

        try:
            all_users: dict[str, User] = self.local_dao.open_file(
                FilePathEnum.USERS.value[self.host.value]
            )

            if email not in all_users:
                raise ValueError("There is no account with this email... please sign in.")

            password_hash = str(bcrypt.hashpw(password.encode("utf-8"), self.password_salt))
            if all_users[email]["password"] != password_hash:
                raise ValueError("Password is incorrect")

            authentication = self.__encode(all_users[email]["username"], self.secret)
            return {
                "email": all_users[email]["email"],
                "username": all_users[email]["username"],
                "user_id": all_users[email]["user_id"],
                "profile": {
                    **all_users[email]["profile"]
                },
                "personal_stores": all_users[email]["personal_stores"],
                "authentication": {
                    **authentication
                }
            }

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Failed to login user %s", e)
            raise e

    def sign_up(self, _obj, _info, email: str, username: str, password: str):
        """
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
        """
        try:
            self.__validate_input("email", email)
            self.__validate_input("username", username)
            self.__validate_input("password", password)
        except ValueError as e:
            self.logger.error("Failed to validate input %s", e)
            raise e

        try:
            all_users: dict[str, User] = self.local_dao.open_file(
                FilePathEnum.USERS.value[self.host.value]
            )

            if email in all_users:
                raise ValueError("There is already an account with this email... please login.")

            password_hash = str(bcrypt.hashpw(password.encode("utf-8"), self.password_salt))
            all_users[email] = User({
                "email": email,
                "username": username,
                "password": password_hash,
                "user_id": str(uuid.uuid4()),
                "profile": {
                    "picture": None,
                    "banner": None,
                    "color": None,
                    "theme": None
                },
                "personal_stores": []
            })
            self.local_dao.save_file(FilePathEnum.USERS.value[self.host.value], all_users)

            authentication = self.__encode(all_users[email]["username"], self.secret)
            return {
                "email": all_users[email]["email"],
                "username": all_users[email]["username"],
                "user_id": all_users[email]["user_id"],
                "profile": {
                    **all_users[email]["profile"]
                },
                "personal_stores": all_users[email]["personal_stores"],
                "authentication": {
                    **authentication
                }
            }

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Failed to sign up user %s", e)
            raise e

    def get_user(self, _obj, _info, username: str):
        """
        Gets the user with the given username

        Parameters:
        - username (str): The user to get

        Returns:
        - dict: The user's data

        Exceptions:
        - ValueError: If the user does not exist
        - FileNotFoundError: If the file is not found
        - json.JSONDecodeError: If the JSON file has an error
        """
        try:
            all_users: dict[str, User] = self.local_dao.open_file(
                FilePathEnum.USERS.value[self.host.value]
            )
            user_data = next(
                (user for user in all_users.values() if user.get("username") == username),
                None
            )
            if not user_data:
                raise ValueError("User does not exist")

            return {
                "email": user_data["email"],
                "username": user_data["username"],
                "user_id": user_data["user_id"],
                "profile": {
                    **user_data["profile"]
                },
                "personal_stores": user_data["personal_stores"]
            }

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Failed to get user %s", e)
            raise e

    def refresh_token(self, _obj, _info, username: str, refresh_token: str):
        """
        Refreshes the user's token using the refresh token, and sends back the new
        authentication data.

        Parameters:
        - username (str): user's name
        - refresh_token (str): the provided refresh token

        Returns:
        - dict: the user's new authentication data

        Exceptions:
        - jwt.InvalidTokenError: If the provided refresh token is not valid
        """
        if self.decode_user(refresh_token, self.refresh_secret) is None:
            raise jwt.InvalidTokenError("Refresh Token is not valid... cannot get a new token")
        return self.__encode(username, self.secret)

