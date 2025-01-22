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
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
