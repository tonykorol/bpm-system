import datetime
from typing import Any

import jwt

from src.config import settings


def encode_jwt(
        payload: dict,
        key: str = settings.JWT_SECRET,
        algorithm: str = settings.JWT_ALGORITHM,
        expires_in: int = settings.token_expires_minutes,
) -> str:
    """Encode a JWT token with the given payload, key, algorithm, and expiration time.

    Args:
        payload (dict): The data to include in the token.
        key (str, optional): The secret key to sign the token. Defaults to the value in settings.JWT_SECRET.
        algorithm (str, optional): The algorithm used to sign the token. Defaults to the value in settings.JWT_ALGORITHM.
        expires_in (int, optional): The expiration time of the token in minutes. Defaults to the value in settings.token_expires_minutes.

    Returns:
        str: The encoded JWT token.

    This function adds `exp` (expiration time) and `iat` (issued at) claims to the payload, and returns the encoded token.

    """
    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    expire = now + datetime.timedelta(minutes=expires_in)
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, key, algorithm)


def decode_jwt(
        token: str,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
) -> dict[str | Any]:
    """Decode a JWT token and return its payload.

    Args:
        token (str): The JWT token to decode.
        key (str, optional): The secret key to verify the token. Defaults to the value in settings.JWT_SECRET.
        algorithm (str, optional): The algorithm used to verify the token. Defaults to the value in settings.JWT_ALGORITHM.

    Returns:
        dict: The decoded payload of the JWT token.

    Raises:
        ValueError: If the token has expired or is invalid.

    """
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
