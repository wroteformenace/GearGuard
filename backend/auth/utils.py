from passlib.context import CryptContext
from datetime import timedelta, datetime
from backend.config import Config
import jwt
import uuid
import logging

ACCESS_TOKEN_EXPIRY = 3600
# This CryptContext class is used to define the method to be used to hash the password with.
# This class is later used in the functions to perform the hashing algorithms.
passwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

def generate_hash_password(password: str) -> str:
    hashed_passwd = passwd_context.hash(password)
    return hashed_passwd


def verify_password(password: str, hashed_passwd: str) -> bool:
    return passwd_context.verify(password, hashed_passwd)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = dict()
    # Payload is generated to create an access_token
    payload["user"] = user_data,
    payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh # Specifies the distinction between refresh and access tokens.

    # Encoding the token using the payload and the header which includes key and algorithm from the Config file.
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

# This decodes the given token to verify.
def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None